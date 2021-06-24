import math

import logomaker
import matplotlib.pyplot as plt
import numpy as np

if __name__ == "__main__":
    ww_df = logomaker.get_example_matrix('ww_information_matrix',
                                         print_description=False)
    print(ww_df.shape)


    # fig, axs = plt.subplots(2)
    # fig.suptitle('Vertically stacked subplots')
    # www_logo1 = logomaker.Logo(ww_df[0:15],
    #                      color_scheme='NajafabadiEtAl2017',
    #                      vpad=.1,
    #                      width=.8)
    # www_logo2 = logomaker.Logo(ww_df[15:30],
    #                           color_scheme='NajafabadiEtAl2017',
    #                           vpad=.1,
    #                           width=.8)
    # axs[0] = www_logo1
    # axs[1] = www_logo2
    # plt.show()

    num_cols = 1
    num_rows = 3
    width_per_col = 700
    height_per_row = 150
    fig = plt.figure()

    ax1 = plt.subplot2grid((num_rows, num_cols), (0, 0))
    ax2 = plt.subplot2grid((num_rows, num_cols), (1, 0))
    ax3 = plt.subplot2grid((num_rows, num_cols), (2, 0))

    amount = ww_df.shape[0]/3.0
    logomaker.Logo(ww_df[0:math.floor(amount)],
                   ax=ax1,
                   show_spines=False)
    logomaker.Logo(ww_df[math.floor(amount):math.floor(2*amount)],
                   ax=ax2,
                   show_spines=False)
    logomaker.Logo(ww_df[math.floor(2*amount):],
                   ax=ax3,
                   show_spines=False)
    fig.suptitle('Test Title', fontsize=16)

    plt.show()

