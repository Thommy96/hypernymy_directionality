import pickle
import time
from tqdm import tqdm
from collections import OrderedDict
from operator import itemgetter
import random
from docopt import docopt

def main():
    args = docopt("""Create 
    - N slices sorted after relative frequency difference
    - three additional slices with relative frequency difference >0, <0 and 0
    - 11 sets with different frequency biases in steps of 10%
    and save as pickle files
    
    Usage:
        slices_freqBias.py <results_freq> <dataset_file> <N_slices> <output_directory_slices> <output_directory_sets>
        
    Arguments:
        <results_freq> = pickled word frequency results
        <dataset_file> = pickled data set
        <N_slices> = number of slices to create
        <output_directory_slices> = directory to save pickled slices
        <output_directory_sets> = directory to save pickled sets
    
    """)

    #get arguments and options
    results_freq = args['<results_freq>']
    dataset_file = args['<dataset_file>']
    N_slices = int(args['<N_slices>'])
    output_directory_slices = args['<output_directory_slices>']
    output_directory_sets = args['<output_directory_sets>']

    freqBias = FreqBias(results_freq, dataset_file)
    print("Creating slices...")
    subDicts = freqBias.divide(N_slices)
    i = 1
    for subDict in subDicts:
        sl = set(subDict.keys())
        filenameSLice = str(output_directory_slices) + "/slice" + str(i) + ".p"
        save_to_pickle(sl, filenameSLice)
        i += 1
    print("Created slices and saved")

    print("Creating additional slices...")
    zeroSlices = freqBias.point_zero()
    grTZ = zeroSlices[0]
    zero = zeroSlices[1]
    smTZ = zeroSlices[2]
    filenamGrTZ = str(output_directory_slices) + "/greaterZero.p"
    filenameZero = str(output_directory_slices) + "/zero.p"
    filenameSmTZ = str(output_directory_slices) + "/smallerZero.p"
    save_to_pickle(grTZ, filenamGrTZ)
    save_to_pickle(zero, filenameZero)
    save_to_pickle(smTZ, filenameSmTZ)
    print("Created additional slices and saved")

    #every run uniq because of random!!
    print("Creating sets...")
    for i in range(0, 11):
        sizeGrTZ = len(smTZ) * (i/10)
        sizeSmTZ = len(smTZ) - sizeGrTZ
        sizeGrTZ = int(round(sizeGrTZ, 0))
        sizeSmTZ = int(round(sizeSmTZ, 0))

        randomGrTZ = set(random.sample(grTZ, k=sizeGrTZ))
        randomSmTZ = set(random.sample(smTZ, k=sizeSmTZ))
        biasSet = randomGrTZ | randomSmTZ

        filenameSet = str(output_directory_sets) + "/set" + str(i*10) + ".p"
        save_to_pickle(biasSet, filenameSet)
    print("Created sets and saved")


class FreqBias:

    def __init__(self, results_freq, dataset_file):
        """
        
        :param results_freq: word frequency results
        :param dataset_file: data set file
        """
        print("Loading freq results and data set...")
        self.resultsFrequency = read_from_pickle(results_freq)
        self.dataset = read_from_pickle(dataset_file)
        print("Loaded freq results and data set")

    def freq_diff(self):
        """
        Calculate word frequency differences
        :return: word frequency differences as dictionary
        """
        results = {}

        for pair in self.dataset:
            hypo = pair[0]
            hyper = pair[1]
            results[pair] = self.resultsFrequency[hyper] - self.resultsFrequency[hypo]

        return results

    def sort_freqDiff(self):
        """
        Sort word frequency differences
        :return: sorted word frequency differences as ordered dict
        """
        freqDiff = self.freq_diff()
        sortedFreqDiff = OrderedDict(sorted(freqDiff.items(), key=itemgetter(1), reverse=True))

        return sortedFreqDiff

    def divide(self, n:int):
        """
        Divide sorted word pairs into slices
        :param n: numver of slices
        :return: list of slices as dictionaries
        """
        sortedFreqDiff = self.sort_freqDiff()
        sortedFreqDiffList = list(sortedFreqDiff.items())
        num = len(sortedFreqDiffList)
        subDicts = []
        i = 0
        while num > 0 and n > 0:
            slice = round(num / n)
            subDict = dict(sortedFreqDiffList[i:i + slice])
            subDicts.append(subDict)

            n = n - 1
            num = num - slice
            i = i + slice
        return subDicts

    def point_zero(self):
        """
        Divide word pairs into word frequency difference >0, <0 and 0
        :return: 
        """
        freqDiff = self.freq_diff()
        grTZ = set()
        zero = set()
        smTZ = set()
        for pair, diff in freqDiff.items():
            if diff > 0:
                grTZ.add(pair)
            elif diff == 0:
                zero.add(pair)
            elif diff < 0:
                smTZ.add(pair)
            else:
                print(diff)
        return grTZ, zero, smTZ

def read_from_pickle(file: str):
    """
    this function reads an object from a pickle file and returns it
    :param file: the file containing the object
    :return obj: the object
    """
    obj = pickle.load(open(file, "rb"))
    return obj


def save_to_pickle(obj, file: str):
    """
    this function saves an object to a pickle file
    :param obj: the object
    :param file: the file to save the object
    """
    pickle.dump(obj, open(file, "wb"), protocol=4)

if __name__ == '__main__':
    main()
