import dataclasses
import Bio
import random
from Bio.Seq import Seq
# http://www.tiem.utk.edu/~gross/bioed/webmodules/aminoacid.htm
# Distribution of AA in Human body

AMINO_ACID_DIST = {
    "A": 0.074,
    "C": 0.033,
    "D": 0.059,
    "E": 0.058,
    "F": 0.04,
    "G": 0.074,
    "H": 0.029,
    "I": 0.038,
    "K": 0.072,
    "L": 0.076,
    "M": 0.018,
    "N": 0.044,
    "P": 0.05,
    "Q": 0.037,
    "R": 0.042,
    "S": 0.081,
    "T": 0.062,
    "W": 0.013,
    "Y": 0.033,
    "V": 0.068,
    "X": 0,
    "-": 0}
import cdr_annotation
import toolz
CDR_METHODS = [cdr_annotation.find_cdr1, cdr_annotation.find_cdr2, cdr_annotation.find_cdr3]
def get_num_of_mutation(sequence, data):
    """
    :param sequence: String of given seq
    :param data: list of sequences from the DB with same length
    :return: retuning number of mutation to apply on given sequence
    """
    return 3

def calc_mutate_sequence(sequence: str, num_of_mutations_to_perform: int):
    list_seq = list(sequence)
    for _ in range(num_of_mutations_to_perform):
        rand_cdr_method = random.choice(CDR_METHODS)
        [left_cdr, right_cdr] = rand_cdr_method(sequence=sequence)
        mutation_aa = random.choices(list(AMINO_ACID_DIST.keys()), list(AMINO_ACID_DIST.values()))[0]
        rand_position = random.randrange(left_cdr, right_cdr)
        list_seq[rand_position] = mutation_aa
    return "".join(list_seq)