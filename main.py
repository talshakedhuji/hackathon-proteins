# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code. dvD
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
import sys

import tensorflow as tf
from tensorflow.keras import layers
import pickle
import numpy as np
import matplotlib.pyplot as plt
import HackatonUtils as utils

def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press ⌘F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    model = tf.keras.models.load_model('./TrainedNanoNet')
    model.summary()
    # predict
    import os

    seq_input = sys.argv[1]
    net_input = utils.generate_input("", False);

    predict_dist, _, _, _ = model.predict(np.asarray([net_input]))

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
