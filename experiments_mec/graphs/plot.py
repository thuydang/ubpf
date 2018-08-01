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

def average_all():
    data = collections.defaultdict(dict)
    names = list()
    x = [0,1,2]
    avg_of_name = list()


    for filename in list_files():
    #for filename in filenames:
        fullpath = os.path.join(_result_data_dir, filename)
        fin = open(fullpath, "r")
        #data.update(filename = pickle.load(fin))
        data[filename] = pickle.load(fin)
        fin.close()


    for filename, dictionary in data.iteritems():
        print "%s" % filename
        names.append(filename)

        #x = dictionary.keys()
        y = [item[0] for item in dictionary.values()] # https://docs.python.org/2/tutorial/datastructures.html#list-comprehensions
        avg_of_name.append(sum(y)/float(len(y)))
        print sum(y)/float(len(y))

    n_groups = 1

    fig, ax = plt.subplots()

    index = np.arange(n_groups)
    #bar_width = 0.35
    bar_width = 0.8

    rects1 = plt.bar(names, avg_of_name, bar_width, color='red')

    #rects1 = plt.bar(index, avg_of_name.pop(0), bar_width, color='red',
    #    label='N1', alpha= 0.8)
    #rects2 = plt.bar(index + bar_width, avg_of_name.pop(0), bar_width, color='green',
    #    label='N2', alpha= 0.8)
    #rects3 = plt.bar(index + 2*bar_width, avg_of_name.pop(0), bar_width, color='black',
    #    label='N3', alpha= 0.8)

    #plt.xlabel('Word')
    plt.ylabel('Average CPU time')
    plt.title('Average CPU time of MM operations')
    #ax.set_xticks(np.add(x, (bar_width / 2)))
    ax.set_xticks(np.add(x, (0)))
    #ax.set_xticklabels(names)
    ax.set_xticklabels(('MM Trigger', 'Measurement', 'Flow Update'))
    #plt.xticks(index + bar_width, ('The', 'Be', 'And', 'Of', 'A'))
    plt.legend()

    for rect in rects1:
        height = rect.get_height()
        ax.text(rect.get_x() + rect.get_width()/2., 0.90*height,
                '%.3f' % float(height*1000) + "ms", ha='center', va='bottom')
    #for rect in rects2:
    #    height = rect.get_height()
    #    ax.text(rect.get_x() + rect.get_width()/2., 0.99*height,
    #            '%d' % (height*1000) + "ms", ha='center', va='bottom')
    #for rect in rects3:
    #    height = rect.get_height()
    #    ax.text(rect.get_x() + rect.get_width()/2., 0.99*height,
    #            '%d' % (height*1000) + "ms", ha='center', va='bottom')
    plt.tight_layout()

    #plt.show()
    plt.savefig('avg.eps', format='eps', dpi=1000)



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

    # Print data
    #pprint.pprint(data)

    fig, ax = plt.subplots()
    #markers = ['x','+','*', 'p', 'd','x','+']
    markers = ['x','+','o','*', 'p', 'd','^','.']
    colors = ['red','green','black']

    for filename, dictionary in data.iteritems():
        print "%s" % filename
        x = dictionary.keys()
        y = [item[0] for item in dictionary.values()] # https://docs.python.org/2/tutorial/datastructures.html#list-comprehensions

        #plt.scatter(x,y, label='CPU time', color='k', s=15, marker="o")
        #ax.scatter(x,y, label=filename, color='k', s=15, marker="o")
        #ax.scatter(x,y, c=np.random.rand(3,), s=5, marker=markers.pop(), label=filename)
        ax.scatter(x,y, c=colors.pop(), s=5, marker=markers.pop(), label=filename)

    # scaling
    #plt.yticks(np.arange(min, max, step))
    plt.ylim(0.0001, 0.002)

    plt.xlabel('MM event')
    plt.ylabel('cpu time (s)')
    plt.title('CPU time of MM operations  ')

    #plt.xlabel('x')
    #plt.ylabel('y (s)')
    #plt.title('CPU time for paket match and match + actions')
    #plt.legend()

    #legend = plt.legend(loc='upper center', shadow=True, fontsize='x-large')
    legend = ax.legend(loc='upper right', shadow=False, fontsize='x-small')
    # Put a nicer background color on the legend.
    #legend.get_frame().set_facecolor('#00FFCC')

    #plt.show()
    plt.savefig('all_scatter.eps', format='eps', dpi=1000)



def main():
    #for filename in list_files():
    #    plot_file(filename)

    plot_all()
    average_all()

if __name__ == "__main__":
    main()
