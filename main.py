import sys
import math
import pandas as pd
import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt
import HackatonUtils as utils
import seq_mutation
from Bio.PDB import Polypeptide
from Bio.SVDSuperimposer import SVDSuperimposer
import subprocess
import random
from tensorflow.keras import layers
import pickle
import argparse
import matplotlib
import FileUtils
import os
import statistics
import logomaker
import glob

HEADER = "HEADER    IMMUNE SYSTEM - NANOBODY                           \nTITLE     COMPUTATIONAL MODELING     \nREMARK 777 MODEL GENERATED BY NANONET \n"
ATOM_LINE = "ATOM{}{}  CA  {} H{}{}{}{:.3f}{}{:.3f}{}{:.3f}  1.00 0.00           C\n"
END_LINE = "END"

AA_NAMES = ["A", "C", "D", "E", "F", "G", "H", "I", "K", "L", "M", "N", "P", "Q", "R", "S", "T", "W", "Y", "V"]
# def create_pdb_from_seq(model, sequence, file_path):
#     net_input = utils.generate_input("", False);
#     predict_dist, _, _, _ = model.predict(np.asarray([net_input]))
#     return predict_dist


def matrix_to_pdb(pdb_file, seq, coord_matrix):
    """
    translates a matrix of Ca x,y,z coordinates to PDB format
    :param pdb_file: pdb file to write to
    :param seq: Nb sequence
    :param coord_matrix: NanoNet output
    :return: None
    """
    pdb_file.write(HEADER)
    seq = utils.pad_seq(seq)
    i = 1
    for aa in range(len(seq)):
        if seq[aa] != "-":
            first_space = (7 - len(str(i))) * " "
            second_space = (4 - len(str(i))) * " "
            third_space = (12 - len("{:.3f}".format(coord_matrix[aa][0]))) * " "
            forth_space = (8 - len("{:.3f}".format(coord_matrix[aa][1]))) * " "
            fifth_space = (8 - len("{:.3f}".format(coord_matrix[aa][2]))) * " "
            if seq[aa] == "X":
                three = "UNK"
            else:
                three = Polypeptide.one_to_three(seq[aa])
            pdb_file.write(ATOM_LINE.format(first_space, i, three, second_space, i, third_space, coord_matrix[aa][0],forth_space, coord_matrix[aa][1],fifth_space, coord_matrix[aa][2]))
            i += 1
    pdb_file.write(END_LINE)


def predict(nanonet, sequence):
    """
    Preform prediction using the nanonet model
    :param nanonet: the trained model
    :param sequence: input sequence
    :return: predicted coordinates
    """
    return nanonet.predict(np.array([utils.generate_input(sequence, fasta=False)]))[0]


def rmsd_calc(coords1, coords2):
    """
    calculates the RMSD score of the 2 given sequences structural alignment
    :param coords1: first seq coordinates
    :param coords2: second seq coordinates
    :return: RMSD score
    """
    sup = SVDSuperimposer()
    sup.set(np.array(coords1, "f"), np.array(coords2, "f"))
    sup.run()
    return float("{:0.3f}".format(sup.get_rms()))


def present_rmsd(results, output_directory):
    """
    plots the RMSDs of the different sequences
    :param results: list of RMSD scores
    :return:
    """
    plt.xlabel('mutation id')
    plt.ylabel('RMSD')
    plt.title('RMSD vs mutation id')
    rmsds = tuple(map(lambda x: x["rmsd"], results))
    ids = tuple(map(lambda x: x["ID"], results))
    plt.plot(ids, rmsds)
    plt.show()
    plt.savefig(output_directory + '/rmsd_by_id.png')

def present_mut_dist(distribution, output_directory):
    """
    plots the mutations distribution
    :param distribution: the data to plot
    :param output_directory: the output directory
    """
    plt.xlabel('Position Index')
    plt.ylabel('Mutations Counter')
    plt.title('RMSD vs mutation id')
    rmsds = tuple(map(lambda x: x["rmsd"], results))
    ids = tuple(map(lambda x: x["ID"], results))
    plt.plot(ids, rmsds)
    plt.show()
    plt.savefig(output_directory + '/rmsd_by_id.png')


def print_report(file, data):
    """
    print to console the mutated sequence's info
    :param file: file to print into
    :param data: the mutated sequence's info to export
    """
    file.write("ID: " + str(data["ID"]) + "\n")
    file.write("# Of Changes Made: " + str(data["num_of_changes"]) + "\n")
    file.write("Mutation Made: " + "\n")
    file.write(str(data["mutations_by_position"]) + "\n")
    file.write("Mutated Sequence: " + str(data["mutate_seq"]) + "\n")
    file.write("Output File Name: " + str(data["file_name"]) + "\n")
    file.write("RMSD: " + str(data["rmsd"]) + "\n")
    file.write("\n")


def present_summary_figs(results, seq_len_distribution, output_directory, sequence):
    present_mut_dist(seq_len_distribution, output_directory)
    present_rmsd(results, output_directory)
    present_score_by_mutation_amount(results, output_directory)
    present_AA_composition(results, output_directory, sequence)


def present_AA_composition(results, output_directory, sequence):
    scores = (map(lambda x: x["rmsd"], results))
    median_score = statistics.median(scores)
    good = []
    bad = []
    for result in results:
        if result["rmsd"] > median_score:
            bad.append(result)
        else:
            good.append(result)

    present_logo(good, sequence, output_directory, "Good")
    present_logo(bad, sequence, output_directory, "Bad")


def present_logo(results, sequence, output_directory, prefix):
    counts_map = {}
    for aa in AA_NAMES:
        counts_map[aa] = np.zeros(len(sequence))
    for res in results:
        seq = res["mutate_seq"]
        for i in range(len(seq)):
            aa = seq[i]
            if aa != sequence[i]:
                counts_map[aa][i] += 1

    amount = float(len(results))
    for aa in counts_map:
        for i in range(len(counts_map[aa])):
            counts_map[aa][i] = counts_map[aa][i]/amount

    df = pd.DataFrame.from_dict(counts_map)

    size = df.shape[0] / 3
    num_cols = 1
    num_rows = 3

    plt.close()
    fig = plt.figure()
    fig.set_size_inches(14, 7.5)
    fig.suptitle(prefix + ' mutations AA freq.', fontsize=16)
    ax1 = plt.subplot2grid((num_rows, num_cols), (0, 0))
    ax2 = plt.subplot2grid((num_rows, num_cols), (1, 0))
    ax3 = plt.subplot2grid((num_rows, num_cols), (2, 0))

    logomaker.Logo(df[0:math.floor(size)],
                   ax=ax1,
                   color_scheme='NajafabadiEtAl2017',
                   show_spines=False)
    logomaker.Logo(df[math.floor(size):math.floor(2*size)],
                   ax=ax2,
                   color_scheme='NajafabadiEtAl2017',
                   show_spines=False)
    logomaker.Logo(df[math.floor(2*size):],
                   ax=ax3,
                   color_scheme='NajafabadiEtAl2017',
                   show_spines=False)

    plt.show()
    plt.savefig(output_directory + '/' + prefix + '_freq.png')

def present_score_by_mutation_amount(results, output_directory):
    # mutations_by_position = tuple(map(lambda x: x["mutations_by_position"], results))
    # mutations_by_position

    scores_by_lengths = {}
    for res in results:
        num_of_mutation = res["num_of_changes"]
        if num_of_mutation in scores_by_lengths:
            scores_by_lengths[num_of_mutation].append(res["rmsd"])
        else:
            scores_by_lengths[num_of_mutation] = [res["rmsd"]]

    means = []
    lengths = []
    for key in scores_by_lengths:
        means.append(sum(scores_by_lengths[key])/len(scores_by_lengths[key]))
        lengths.append(key)

    plt.xlabel('mutations amount')
    plt.ylabel('mean RMSD')
    plt.title('mean RMSD by mutations amount')
    plt.bar(lengths, means)
    plt.show()
    plt.savefig(output_directory + '/mean_rmsd_by_amount.png')

def clear_ouput_directory(path):
    try:
        files = glob.glob(path + "/*")
        for f in files:
            os.remove(f)
    except:
        raise SystemExit('Error: could not delete the content of the output directory')


def run(model_path, fasta):

    nanonet = tf.keras.models.load_model(model_path)
    # nanobody sequence
    file_name = "./SolvedNbs/Nb34/Nb34.fa"
    sequence = utils.get_sequence(fasta)

    # Create output directory
    output_directory = "./outputs"
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)
    else:
        clear_ouput_directory(output_directory)

    # ca coordinates
    ca_coords = predict(nanonet, sequence)
    # create ca pdb file
    ca_mutated_file_name = "./outputs/mutated_{}.pdb"
    original_file_name = "./outputs/original.pdb".format(file_name.split(".")[0])
    with open(original_file_name, "w") as ca_file:
        matrix_to_pdb(ca_file, sequence, ca_coords)
    print("PDB of original sequence was created successfully, file name: original.pdb")
    all_results = []
    f = open('./outputs/summery.txt', 'w')
    seq_by_len = FileUtils.decompress_pickle('seq_by_len_comp.pbz2')
    num_of_mutations = 10000
    seq_len_distribution = seq_mutation.calc_distribution_for_sequance(sequence, seq_by_len)
    for i in range(num_of_mutations):
        data = {}
        data["ID"] = i
        data["num_of_changes"] = seq_mutation.get_num_of_mutation(seq_len_distribution)
        data["mutate_seq"] = seq_mutation.calc_mutate_sequence(sequence, data["num_of_changes"])
        data["coords"] = predict(nanonet, data["mutate_seq"])
        data["file_name"] = ca_mutated_file_name.format(i)
        data["rmsd"] = rmsd_calc(ca_coords, data["coords"])
        data["mutations_by_position"] = seq_mutation.mutations_by_position(sequence, data["mutate_seq"])
        with open(data["file_name"], "w") as ca_mutate_file:
            matrix_to_pdb(ca_mutate_file, data["mutate_seq"], data["coords"])
        all_results.append(data)
        print_report(f, data)
    f.close()
    present_summary_figs(all_results, seq_len_distribution, output_directory, sequence)


def temp_run(): #TODO(rachel): Change to main
    return run("./TrainedNanoNet", "./SolvedNbs/Nb34/Nb34.fa", )

if __name__ == "__main__":
    """
       receives path to a Nb fasta file and a path to a trained neural network and creates a pdb file (Ca only) according to
       the network prediction. the output file name is: "<fasta file name>_nanonet_ca.pdb"
       """
    # parser = argparse.ArgumentParser()
    # parser.add_argument("fasta", help="Nb fasta file")
    # parser.add_argument("network", help="nanonet trained model")
    #
    # args = parser.parse_args()
    # run(args.network, args.fasta)
    temp_run()
