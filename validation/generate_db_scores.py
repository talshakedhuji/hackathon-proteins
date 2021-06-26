import pickle
import pandas as pd
from tqdm import tqdm

import HackatonUtils as utils
import cdr_annotation
import db_analysis


def search_cdr(sequences, cdr_sequence):
    """
    searchs the given cdr sequence in the sequences
    :param sequences: (DB) sequences
    :param cdr_sequence: cdr sequence
    :return: 1 if the cdr sequence exists in the DB sequences and 0 otherwise
    """
    for seq in sequences:
        if cdr_sequence in seq:
            return 1
    return 0


def calculate_cdr_score(sequences, sequence, cdr_seq):
    """
    return 1 if the cdr is the same as the original sequence or if the cdr is in the DB sequences
    :param sequences: (DB) sequences
    :param sequence: original sequence
    :param cdr_seq: cdr sequence
    :return: 1 if the cdr is the same as the original sequence or if the cdr is in the DB sequences
    """
    if cdr_seq in sequence:
        return 1
    else:
        return search_cdr(sequences, cdr_seq)


def calculate_score(sequences, sequence, mut_seq, cdr1_region, cdr2_region, cdr3_region):
    """
    return the score for the mutated sequence.
    the score is composed of 3 indicators (for each one of the CDRs) and the sum of the indicators
    :param sequences: db sequences
    :param sequence: the original sequence
    :param mut_seq: the mutated sequence
    :param cdr1_region: CDR1 region
    :param cdr2_region: CDR2 region
    :param cdr3_region: CDR3 region
    :return: the score for the mutated sequence
    """
    cdr1_seq = mut_seq[cdr1_region[0]:cdr1_region[1]]
    cdr2_seq = mut_seq[cdr2_region[0]:cdr2_region[1]]
    cdr3_seq = mut_seq[cdr3_region[0]:cdr3_region[1]]

    cdr_hits = [calculate_cdr_score(sequences, sequence, cdr1_seq),
                calculate_cdr_score(sequences, sequence, cdr2_seq),
                calculate_cdr_score(sequences, sequence, cdr3_seq)]
    score = sum(cdr_hits)
    return [cdr_hits[0], cdr_hits[1], cdr_hits[2], score]


if __name__ == "__main__":

    with open('../outputs/results.pickle', 'rb') as handle:
        results = pickle.load(handle)

    sorted_results = sorted(results, key=lambda x: x["rmsd"])
    sequence = utils.get_sequence("../SolvedNbs/Nb34/Nb34.fa")

    cdr1_region = cdr_annotation.find_cdr1(sequence)
    cdr1_seq = sequence[cdr1_region[0]:cdr1_region[1]]
    cdr2_region = cdr_annotation.find_cdr2(sequence)
    cdr2_seq = sequence[cdr2_region[0]:cdr2_region[1]]
    cdr3_region = cdr_annotation.find_cdr3(sequence)
    cdr3_seq = sequence[cdr3_region[0]:cdr3_region[1]]

    print(sequence)
    print("CDR1:")
    print(cdr1_region)
    print(cdr1_seq)
    print("CDR2:")
    print(cdr2_region)
    print(cdr2_seq)
    print("CDR3:")
    print(cdr3_region)
    print(cdr3_seq)

    # validating that the original seq. cdrs are in the DB:

    db_filename = "../AboutMillionSequencesNew.fasta"
    sequences = db_analysis.get_sequences(db_filename)
    print(search_cdr(sequences, cdr1_seq))
    print(search_cdr(sequences, cdr2_seq))
    print(search_cdr(sequences, cdr3_seq))

    print(len(sorted_results))

    # filtering duplicated sequences:

    # unique = []
    # for res in sorted_results:
    #     if res['mutate_seq'] not in unique:
    #         unique.append(res['mutate_seq'])
    # print(len(unique))
    # with open('unique_results.pickle', 'wb') as handle:
    #     pickle.dump(unique, handle)

    # generate scores:
    with open('unique_results.pickle', 'rb') as handle:
        unique = pickle.load(handle)
    print(len(unique))

    scores = []
    for i in tqdm(range(0, len(unique)), desc=f'Calculating CDR scores for mutation sequences...'):
        mut_seq = unique[i]
        scores.append(calculate_score(sequences, sequence, mut_seq, cdr1_region, cdr2_region, cdr3_region))

    with open('all_scores.pickle', 'wb') as handle:
        pickle.dump(scores, handle)

    print(scores)
