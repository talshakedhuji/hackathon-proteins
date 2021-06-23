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

def get_num_of_diffs(seq1, seq2):
    """
       :param seq1: first sequence
       :param seq2: second sequence
       :return: number of mutation btw the two sequences
       """
    return sum(1 for a, b in zip(seq1, seq2) if a != b)
MAX_CHANGES = 5
def get_num_of_mutation(sequence, len_to_seq):
    """
    :param sequence: String of given seq
    :param data: list of sequences from the DB with same length
    :return: number of mutation to apply on given sequence
    """
    x = [0]*MAX_CHANGES
    for record in len_to_seq[len(record)]:
        diffs = get_num_of_diffs(sequence, record)
        if diffs > MAX_CHANGES or diffs == 0:
            continue
        x[diffs-1] += 1
    return random.choices(numpy.array(range(MAX_CHANGES))+1, k=1, weights=x)[0]


def calc_mutate_sequence(sequence: str, num_of_mutations_to_perform: int):
    list_seq = list(sequence)
    for _ in range(num_of_mutations_to_perform):
        rand_cdr_method = random.choice(CDR_METHODS)
        [left_cdr, right_cdr] = rand_cdr_method(sequence=sequence)
        rand_position = random.randrange(left_cdr, right_cdr)
        original_aa = list_seq[rand_position]
        temp_AA_dist = AMINO_ACID_DIST.copy()
        temp_AA_dist.pop(original_aa)
        mutation_aa = random.choices(list(temp_AA_dist.keys()), list(temp_AA_dist.values()))[0]
        list_seq[rand_position] = mutation_aa
    return "".join(list_seq)