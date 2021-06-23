from Bio import SeqIO
from collections import defaultdict
import pickle as pkl

AA_NAMES = ["A", "C", "D", "E", "F", "G", "H", "I", "K", "L", "M", "N", "P", "Q", "R", "S", "T", "W", "Y", "V", "-",
            "X"]


def get_sequence(fasta_filename_input):
    """
    Returns a list of sequences from the given fasta file
    :param fasta_filename: name of the fasta file to be parsed
    :return: a list of the fasta sequences
    """
    sequences = []
    for seq_record in SeqIO.parse(fasta_filename_input, "fasta"):
        sequence = str(seq_record.seq)
        sequences.append(sequence)
    return sequences


def extract_lengths(sequences):
    """
    Returns the the sequences grouped by their length
    :param sequences: list of aa sequences
    :return: dictionary of sequences by length
    """
    seq_by_length = {}
    for s in sequences:
        length = str(len(s))
        if length in seq_by_length:
            seq_by_length[length].append(s)
        else:
            seq_by_length[length] = [s]
    return seq_by_length


def extract_AA_frequencies(sequences):
    """
    Returns the given sequences AA frequencies
    :param sequences: list of AA sequences
    :return: AA frequency dict
    """
    freq_dict = defaultdict(float)

    count = 0.0
    for seq in sequences:
        for aa in seq:
            freq_dict[aa] += 1
            count += 1

    if count > 0:
        for key in freq_dict:
            freq_dict[key] = freq_dict[key] / count
    return freq_dict


if __name__ == '__main__':
    fasta_filename = "AboutMillionSequencesNew.fasta"
    sequences = get_sequence(fasta_filename)
    seq_by_length = extract_lengths(sequences)
    freq_dict = extract_AA_frequencies(sequences)

    # save data
    with open('Data/seq_by_length.pickle', 'wb') as handle:
        pkl.dump(seq_by_length, handle)

    with open('Data/freq_dict.pickle', 'wb') as handle:
        pkl.dump(freq_dict, handle)

    # # load (for DEBUG)
    # with open('Data/seq_by_length.pickle', 'rb') as handle:
    #     a = pkl.load(handle)
    #
    # with open('Data/freq_dict.pickle', 'rb') as handle:
    #     b = pkl.load(handle)
    #
    # print(a)
    # print(b)
