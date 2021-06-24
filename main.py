import sys
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

HEADER = "HEADER    IMMUNE SYSTEM - NANOBODY                           \nTITLE     COMPUTATIONAL MODELING     \nREMARK 777 MODEL GENERATED BY NANONET \n"
ATOM_LINE = "ATOM{}{}  CA  {} H{}{}{}{:.3f}{}{:.3f}{}{:.3f}  1.00 0.00           C\n"
END_LINE = "END"


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
    sup.set(coords1, coords2)
    sup.run()
    return float("{:0.3f}".format(sup.get_rms()))


def present_rmsd(list_of_rmsds):
    """
    plots the RMSDs of the different sequences
    :param list_of_rmsds: list of RMSD scores
    :return:
    """
    plt.xlabel('mutation id')
    plt.ylabel('RMSD')
    plt.title('RMSD vs mutation id')
    plt.plot(list_of_rmsds)
    plt.show()


def print_report(data):
    """
    print to console the mutated sequence's info
    :param data: the mutated sequence's info to export
    """
    print("# Of Changes Made: " + str(data["num_of_changes"]))
    print("Mutation Made: ")
    print(data["mutations_by_position"])
    print("Mutated Sequence: " + str(data["mutate_seq"]))
    print("Output File Name: " + str(data["file_name"]))
    print("RMSD: " + str(data["rmsd"]))
    print(u'\u2500' * 100)



def present_positions_summary(results):
    present_score_by_mutation_amount(results)


def present_score_by_mutation_amount(results):
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


def run(model_path, fasta):

    nanonet = tf.keras.models.load_model(model_path)
    # nanobody sequence
    file_name = "./SolvedNbs/Nb34/Nb34.fa"
    sequence = utils.get_sequence(fasta)

    # Create output directory
    output_directory = "./outputs"
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    # ca coordinates
    ca_coords = predict(nanonet, sequence)
    # create ca pdb file
    ca_file_name = "./outputs/{}_nanonet_ca.pdb".format(file_name.split(".")[0])
    ca_mutated_file_name = "./outputs/mutated_{}.pdb"
    with open(ca_file_name, "w") as ca_file:
        matrix_to_pdb(ca_file, sequence, ca_coords)
    all_results = []
    seq_by_len = FileUtils.decompress_pickle('seq_by_len_comp.pbz2')
    num_of_mutations = 40
    seq_len_distribution = seq_mutation.calc_distribution_for_sequance(sequence, seq_by_len) 
    for i in range(num_of_mutations):
        data = {}
        mutations_by_position = {}
        data["num_of_changes"] = seq_mutation.get_num_of_mutation(seq_len_distribution)
        data["mutate_seq"] = seq_mutation.calc_mutate_sequence(sequence, data["num_of_changes"], mutations_by_position)
        data["coords"] = predict(nanonet, data["mutate_seq"])
        data["file_name"] = ca_mutated_file_name.format(i)
        data["rmsd"] = rmsd_calc(ca_coords, data["coords"])
        data["mutations_by_position"] = mutations_by_position
        with open(data["file_name"], "w") as ca_mutate_file:
            matrix_to_pdb(ca_mutate_file, data["mutate_seq"], data["coords"])
        all_results.append(data)
        print_report(data)
    present_rmsd(tuple(map(lambda x: x["rmsd"], all_results)))
    present_positions_summary(all_results)


def temp_run(): #TODO(rachel): Change to main
    """
    receives path to a Nb fasta file and a path to a trained neural network and creates a pdb file (Ca only) according to
    the network prediction. the output file name is: "<fasta file name>_nanonet_ca.pdb"
    """
    # parser = argparse.ArgumentParser()
    # parser.add_argument("fasta", help="Nb fasta file")
    # parser.add_argument("network", help="nanonet trained model")

    # args = parser.parse_args()
    return run("./TrainedNanoNet", "./SolvedNbs/Nb34/Nb34.fa", )

if __name__ == "__main__":
    temp_run()
