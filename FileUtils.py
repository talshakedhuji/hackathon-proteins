# import required python modules

import pickle
import uuid
import bz2
import pickle
import _pickle as cPickle


# Pickle a file and then compress it into a file with extension
def compressed_pickle(title, data):
    with bz2.BZ2File(title + '.pbz2', 'w') as f:
        cPickle.dump(data, f)


# Load any compressed pickle file
def decompress_pickle(file):
    data = bz2.BZ2File(file, 'rb')
    data = cPickle.load(data)
    return data


def test():
    objectRep = open("seq_by_length.pickle", "rb")
    object1 = pickle.load(objectRep)
    compressed_pickle("seq_by_len_comp", object1)


def test_load():
    data = decompress_pickle('seq_by_len_comp.pbz2')
    objectRep = open("seq_by_length.pickle", "rb")
    object1 = pickle.load(objectRep)
    print(object1 == data)
