import random
import numpy
import cdr_annotation
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


CDR_METHODS = [cdr_annotation.find_cdr1, cdr_annotation.find_cdr2, cdr_annotation.find_cdr3]
from Bio import pairwise2
def get_num_of_diffs(seq1, seq2):
    """
       :param seq1: first sequence
       :param seq2: second sequence
       :return: number of mutation btw the two sequences
       """
    return sum(1 for a, b in zip(seq1, seq2) if a != b)


def calc_distribution_for_sequence(sequence, len_to_seq):
    """

    :param sequence:
    :param len_to_seq:
    :return:
    """
    MAX_CHANGES = len(sequence)
    x = [0] * MAX_CHANGES
    for record in len_to_seq[str(len(sequence))]:
        diffs = 0
        for cdr_method in CDR_METHODS:
            [ind1, ind2] = cdr_method(sequence)
            [ind1_record, ind2_record] = cdr_method(record)
            sub_seq = sequence[ind1:ind2]
            sub_seq_record = sequence[ind1_record:ind2_record]
            alignments = pairwise2.align.globalxx(sub_seq, sub_seq_record)

            diffs += int(abs(len(sub_seq) - alignments[0].score))
        if diffs > MAX_CHANGES or diffs == 0:
            continue
        x[diffs - 1] += 1
    print("Distribution of mutation was calculated successfully")
    return x

def get_num_of_mutation(distribution):
    """ Get num of mutation
    :param distribution: the mutation distribution
    :return: number of mutation to apply on given sequence
    """
    return random.choices(numpy.array(range(len(distribution)))+1, k=1, weights=distribution)[0]

def get_random_letter():
    """
    return a random AA letter
    :return: aa character
    """
    # return random.choice(tuple(AMINO_ACID_DIST.keys()))
    return random.choices(list(AMINO_ACID_DIST.keys()), list(AMINO_ACID_DIST.values()))[0]


def get_random_position(sequence, positions):
    """
    returns a position that havn't been picked yet
    :param sequence: given sequence
    :param positions: list of "unavailable" posiitons
    :return: a random position under the constraints of unique position for each mutation
    """
    rand_cdr_method = random.choice(CDR_METHODS)
    [left_cdr, right_cdr] = rand_cdr_method(sequence=sequence)
    rand_position = random.randrange(left_cdr, right_cdr)
    while rand_position in positions:
        rand_cdr_method = random.choice(CDR_METHODS)
        [left_cdr, right_cdr] = rand_cdr_method(sequence=sequence)
        rand_position = random.randrange(left_cdr, right_cdr)
    return rand_position

def mutations_by_position(sequence_source:str, dest_sequance:str):
    """
    creates a mutation by position dictionary
    :param sequence_source: the original seq
    :param dest_sequance: the mutated seq
    :return: dictionary of mutations by the position they occurred
    """
    assert len(sequence_source) == len(dest_sequance)
    mutations_by_position = {}
    for i in range(len(sequence_source)):
        if sequence_source[i] != dest_sequance[i]:
            mutations_by_position[str(i)] = (sequence_source[i], dest_sequance[i],)
    return mutations_by_position


def calc_mutate_sequence(sequence: str, num_of_mutations_to_perform: int):
    list_seq = list(sequence)
    positions = set()
    while len(positions) != num_of_mutations_to_perform:
        rand_position = get_random_position(sequence, positions)
        positions.add(rand_position)
        original_aa = list_seq[rand_position]
        mutation_aa = get_random_letter()
        while original_aa == mutation_aa:
            mutation_aa = get_random_letter()
        list_seq[rand_position] = mutation_aa
    return "".join(list_seq)
