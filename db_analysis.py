from Bio import SeqIO
from collections import defaultdict

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
    Returns the counts for each sequences length
    :param sequences: list of aa sequences
    :return: dictionary of seq lengths with counts
    """
    lengths_map = {}
    for s in sequences:
        length = str(len(s))
        if length in lengths_map:
            lengths_map[length] = lengths_map[length] + 1
        else:
            lengths_map[length] = 1
    return lengths_map


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
    length_counts = extract_lengths(sequences)
    print(length_counts)
    freq_dict = extract_AA_frequencies(sequences)
    print(freq_dict)
