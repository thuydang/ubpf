import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pprint
import collections

# use module pickle to save/dump and load a dictionary object
# or just about any other intact object
import pickle


_result_data_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), "../results")

def list_files():
    """
    Return a list of data files under _result_data_dir.
    These strings are suitable to be passed to read().
    """

    result = []
    for dirname, dirnames, filenames in os.walk(_result_data_dir):
        dirname = (os.path.relpath(dirname, _result_data_dir) + '/').replace('./', '')
        for filename in filenames:
            if filename.endswith('.data') and not filename.startswith('.'):
                result.append(dirname + filename)
    return sorted(result)


def plot_file(filename):
    ## Create the test dictionary
    #before_d = {}
    #before_d[1]="Name 1"
    #before_d[2]="Name 2"
    #before_d[3]="Name 3"
    ## pickle dump the dictionary
    #fout = open("dict1.dat", "w")
    ## default protocol is zero
    ## -1 gives highest prototcol and smallest data file size
    #pickle.dump(before_d, fout, protocol=0)
    #fout.close()
    # pickle load the dictionary

    fullpath = os.path.join(_result_data_dir, filename)
    fin = open(fullpath, "r")
    dictionary = pickle.load(fin)
    fin.close()



    x = dictionary.keys()
    y = [item[0] for item in dictionary.values()] # https://docs.python.org/2/tutorial/datastructures.html#list-comprehensions

    fig, ax = plt.subplots()
    #plt.scatter(x,y, label='CPU time', color='k', s=15, marker="o")
    #ax.scatter(x,y, label=filename, color='k', s=15, marker="o")
    ax.scatter(x,y, color='k', s=15, marker="o")

    # scaling
    #plt.yticks(np.arange(min, max, step))
    plt.ylim(0.0005, 0.003)

    plt.xlabel('packet')
    plt.ylabel('cpu time (s)')
    plt.title(filename)

    #plt.xlabel('x')
    #plt.ylabel('y (s)')
    #plt.title('CPU time for paket match and match + actions')
    #plt.legend()

    #legend = plt.legend(loc='upper center', shadow=True, fontsize='x-large')
    legend = ax.legend(loc='upper center', shadow=True, fontsize='x-large')
    # Put a nicer background color on the legend.
    legend.get_frame().set_facecolor('#00FFCC')

    #plt.show()
    plt.savefig(filename+'.eps', format='eps', dpi=1000)

def plot_all():
    ## Create the test dictionary
    #before_d = {}
    #before_d[1]="Name 1"
    #before_d[2]="Name 2"
    #before_d[3]="Name 3"
    ## pickle dump the dictionary
    #fout = open("dict1.dat", "w")
    ## default protocol is zero
    ## -1 gives highest prototcol and smallest data file size
    #pickle.dump(before_d, fout, protocol=0)
    #fout.close()
    # pickle load the dictionary

    data = collections.defaultdict(dict)

    for filename in list_files():
    #for filename in filenames:
        fullpath = os.path.join(_result_data_dir, filename)
        fin = open(fullpath, "r")
        #data.update(filename = pickle.load(fin))
        data[filename] = pickle.load(fin)
        fin.close()

    #pprint.pprint(data)

    fig, ax = plt.subplots()

    for filename, dictionary in data.iteritems():
        print "%s" % filename
        x = dictionary.keys()
        y = [item[0] for item in dictionary.values()] # https://docs.python.org/2/tutorial/datastructures.html#list-comprehensions

        #plt.scatter(x,y, label='CPU time', color='k', s=15, marker="o")
        #ax.scatter(x,y, label=filename, color='k', s=15, marker="o")
        ax.scatter(x,y, c=np.random.rand(3,), s=15, marker="o", label=filename)

    # scaling
    #plt.yticks(np.arange(min, max, step))
    plt.ylim(0.0005, 0.005)

    plt.xlabel('packet')
    plt.ylabel('cpu time (s)')
    plt.title('CPU time for paket match and match + MAC rewrite ')

    #plt.xlabel('x')
    #plt.ylabel('y (s)')
    #plt.title('CPU time for paket match and match + actions')
    #plt.legend()

    #legend = plt.legend(loc='upper center', shadow=True, fontsize='x-large')
    legend = ax.legend(loc='upper right', shadow=False, fontsize='x-small')
    # Put a nicer background color on the legend.
    #legend.get_frame().set_facecolor('#00FFCC')

    #plt.show()
    plt.savefig('all.eps', format='eps', dpi=1000)



def main():
    #for filename in list_files():
    #    plot_file(filename)

    plot_all()

if __name__ == "__main__":
    main()
