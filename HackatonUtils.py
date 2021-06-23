from Bio.PDB import *
import numpy as np
from Bio import SeqIO

# max length of Nb
NB_MAX_LENGTH = 140

# AA dictionary for one-hot encoding
AA_DICT = {"A": 0, "C": 1, "D": 2, "E": 3, "F": 4, "G": 5, "H": 6, "I": 7, "K": 8, "L": 9, "M": 10, "N": 11, "P": 12,
           "Q": 13, "R": 14, "S": 15, "T": 16, "W": 17, "Y": 18, "V": 19, "-": 21, "X": 20}


def pad_seq(seq):
    """
    pads a seq with "-" so it will have length == NB_MAX_LENGTH
    :param seq: Nb sequence (len=<140)
    :return: Nb sequence (len==140)
    """
    seq_len = len(seq)
    up_pad = (NB_MAX_LENGTH - seq_len) // 2
    down_pad = NB_MAX_LENGTH - up_pad - seq_len

    # pad the sequence with '-'
    seq = up_pad * "-" + seq + down_pad * "-"
    return seq


def get_sequence(fasta_filename):
    for seq_record in SeqIO.parse(fasta_filename, "fasta"):
        sequence = str(seq_record.seq)
        return sequence


def get_seq_aa(chain):
    """
    returns the sequence (String) and a list of all the aa residue objects of the given nanobody chain.
    :param chain: BioPython chain object
    :return: sequence, [aa objects]
    """
    aa_residues = []
    seq = ""

    for residue in chain.get_residues():
        aa = residue.get_resname()
        if not is_aa(aa) or not residue.has_id('CA'):
            continue
        elif aa == "UNK":
            seq += "X"
            aa_residues.append(residue)
        else:
            seq += Polypeptide.three_to_one(residue.get_resname())
            aa_residues.append(residue)

    return seq, aa_residues


def generate_input(pdb_fasta, fasta=True):
    """
    receives a fasta file and returns its  sequence in a one-hot encoding matrix (each row is an aa in the sequence, and
    each column represents a different aa out of the 20 aa + 2 special columns).
    :param pdb_fasta: path to a fasta file if fasta=True or sequence (string) if fasta=False
    :return: numpy array of size (NB_MAX_LENGTH * 22)
    """
    if fasta:
        seq = get_sequence(pdb_fasta)
    else:
        seq = pdb_fasta

    if "X" in seq:
        print("Warning, PDB: {}, has unknown aa".format(pdb_fasta))

    # pad the sequence with '-'
    seq = pad_seq(seq)

    # turn in to one-hot encoding matrix
    seq_matrix = np.zeros((NB_MAX_LENGTH, 22))
    for i in range(NB_MAX_LENGTH):
        seq_matrix[i][AA_DICT[seq[i]]] = 1

    return seq_matrix


# TODO!!! - USE THIS FUNCTION ONLY AFTER ALIGNING THE NB TO THE REF MODEL! IF YOU ARE USING IT FOR SOME REASON TALK TO ME FIRST (TOMER)
def generate_label(pdb):
    """
    receives a pdb file and returns its Ca x,y,z coordinates.
    :param pdb: path to a pdb file (nanobody, heavy chain has id 'H')
    :return: numpy array, with size (NB_MAX_LENGTH * 3).
    """

    # load model
    model = PDBParser(QUIET=True).get_structure(pdb, pdb)[0]["H"]

    # get seq and aa residues
    seq, aa_residues = get_seq_aa(model)

    seq_len = len(seq)
    up_pad = (NB_MAX_LENGTH - seq_len) // 2

    labels_matrix = np.zeros((NB_MAX_LENGTH, 3))
    # get the coordinates
    for i in range(seq_len):
        labels_matrix[i+up_pad] = aa_residues[i]["CA"].get_coord()

    return labels_matrix
