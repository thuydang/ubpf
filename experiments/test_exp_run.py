from __future__ import print_function
import os
import pprint
import datetime
import tempfile
import pickle

import struct
import re
from timeit import timeit
from subprocess import Popen, PIPE
from nose.plugins.skip import Skip, SkipTest
from nose.tools import with_setup
import ubpf.assembler
import testdata

'''
Using nosetests to trigger experiment execution.

functions:
* check_datafile: load data and run
* test_datafiles: trigger experiment for all files (call check_datafile by nosetests)
* setup_func, teardown_func: statistic collection
'''

_test_results_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), "./results")
VM = os.path.join(os.path.dirname(os.path.realpath(__file__)), "..", "vm", "test")

# Experiment setup and statistic

#statistics.setdefault(exp_id, []).append(int(time))
statistics = {}
experiment_iteration = 1000
result_file = None
result_filename = None

def check_datafile(filename):
    """
    Given assembly source code and an expected result, run the eBPF program and
    verify that the result matches.
    """
    data = testdata.read(filename)
    if 'asm' not in data and 'raw' not in data:
        raise SkipTest("no asm or raw section in datafile")
    if 'result' not in data and 'error' not in data and 'error pattern' not in data:
        raise SkipTest("no result or error section in datafile")
    if not os.path.exists(VM):
        raise SkipTest("VM not found")

    if 'raw' in data:
        code = ''.join(struct.pack("=Q", x) for x in data['raw'])
    else:
        code = ubpf.assembler.assemble(data['asm'])

    memfile = None

    cmd = [VM]
    if 'mem' in data:
        memfile = tempfile.NamedTemporaryFile()
        memfile.write(data['mem'])
        memfile.flush()
        cmd.extend(['-m', memfile.name])

    cmd.append('-')

    for exp_id in range(0, experiment_iteration):
        vm = Popen(cmd, stdin=PIPE, stdout=PIPE, stderr=PIPE)

        stdout, stderr = vm.communicate(code)
        stderr = stderr.strip()

        ##print timeit(stmt = "subprocess.call('...')", setup = "import subprocess", number = 100)


        if 'error' in data:
            if data['error'] != stderr:
                raise AssertionError("Expected error %r, got %r" % (data['error'], stderr))
        elif 'error pattern' in data:
            if not re.search(data['error pattern'], stderr):
                raise AssertionError("Expected error matching %r, got %r" % (data['error pattern'], stderr))
        else:
            if stderr:
                raise AssertionError("Unexpected error %r" % stderr)

        if 'result' in data:
            if vm.returncode != 0:
                raise AssertionError("VM exited with status %d, stderr=%r" % (vm.returncode, stderr))
            expected = int(data['result'], 0)
            # parse result from stdout: match result;CPU time in second
            #print("vm: %s \n", stdout)
            output = stdout.split(';')
            print("match result: %s; CPU time: %s \n", output[0], output[1])
            result=int(output[0],0)

            # do some statistics
            statistics.setdefault(exp_id, []).append(float(output[1]))

            #result = int(stdout, 0)
            if expected != result:
                raise AssertionError("Expected result 0x%x, got 0x%x, stderr=%r" % (expected, result, stderr))
        else:
            if vm.returncode == 0:
                raise AssertionError("Expected VM to exit with an error code")
    # after for
    if memfile:
        memfile.close()

def setup_func():
    statistics = {}

def teardown_func():
    print("tear down test fixtures", end=" ")

    result_filename = "result_" + datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S") + ".data"
    fullpath = os.path.join(_test_results_dir, result_filename)
    result_file = open(fullpath, "a")

    # pickle dump the dictionary
    # default protocol is zero
    # -1 gives highest prototcol and smallest data file size
    pickle.dump(statistics, result_file, protocol=0)
    result_file.close()
    #pprint.pprint(statistics, stream=result_file)

    print('average match time %f in %d interation: \n' , ( sum( item[0] for item in statistics.values()) / experiment_iteration, experiment_iteration ) )
    #result_file.write("average match time %f in %d interation: \n" % ( sum( item[0] for item in statistics.values()) / experiment_iteration, experiment_iteration ) )

    result_file.close()

@with_setup(setup_func, teardown_func)
def test_datafiles():
    # Nose test generator
    # Creates a testcase for each datafile
    for filename in testdata.list_files():
        yield check_datafile, filename
