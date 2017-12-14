# uBPF

Userspace eBPF VM

[![Build Status](https://travis-ci.org/iovisor/ubpf.svg?branch=master)](https://travis-ci.org/iovisor/ubpf)
[![Coverage Status](https://coveralls.io/repos/iovisor/ubpf/badge.svg?branch=master&service=github)](https://coveralls.io/github/iovisor/ubpf?branch=master)

## About

This project aims to create an Apache-licensed library for executing eBPF programs. The primary implementation of eBPF lives in the Linux kernel, but due to its GPL license it can't be used in many projects.

[Linux documentation for the eBPF instruction set] (https://www.kernel.org/doc/Documentation/networking/filter.txt)

[Instruction set reference] (https://github.com/iovisor/bpf-docs/blob/master/eBPF.md)

This project includes an eBPF assembler, disassembler, interpreter,
and JIT compiler for x86-64.

## Building

Run `make -C vm` to build the VM. This produces a static library `libubpf.a`
and a simple executable used by the testsuite.

## Compiling C to eBPF

You'll need [Clang 3.7] (http://llvm.org/releases/download.html#3.7.0).

    clang-3.7 -O2 -target bpf -c prog.c -o prog.o

You can then pass the contents of `prog.o` to `ubpf_load_elf`, or to the stdin of
the `vm/test` binary.


## Contributing

Please fork the project on GitHub and open a pull request. You can run all the
tests with `nosetests`.

## License

Copyright 2015, Big Switch Networks, Inc. Licensed under the Apache License, Version 2.0
<LICENSE-APACHE or http://www.apache.org/licenses/LICENSE-2.0>.

## MY EXPERIMENT

* create virtualenv
* pip install requirements.txt
* make -C vm
+ run from top folder:
 		nosetests experiments/test_run.py

 		nosetests -vv experiments/test_exp_run.py

* -s to prevent stdout capture by nosetest

### generate pcap, mem, etc:

		cd experiments
    python expand-testcase.py path_under_data/match folder_data
    python expand-testcase.py matchheaders/match data

Generated files are in data folder.

### View pcap
    hexview
		tcpick -C -yP -r tcp_dump.pcap

		tcpdump -qnns 0 -A -r blah.pcap

Use this:

		tcpdump -qnns 0 -X -r serverfault_request.pcap

### Plot
A script reads results as dictionary and draws graphs:
    python plotly.py

