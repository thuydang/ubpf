import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# use module pickle to save/dump and load a dictionary object
# or just about any other intact object
import pickle


_result_data_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), "../results")

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

    plt.scatter(x,y, label='skitscat', color='k', s=25, marker="o")

    plt.xlabel('x')
    plt.ylabel('y (s)')
    plt.title('CPU time for paket match and match + actions')
    plt.legend()
    plt.show()

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

def main():
    for filename in list_files():
        plot_file(filename)

if __name__ == "__main__":
    main()
