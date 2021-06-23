if __name__ == '__main__':
    fasta_filename = "AboutMillionSequencesNew.fasta"
    processed_filename = "AboutMillionSequencesProcessed.fasta"
    name_prefix = "7168_4th_CoV2_BL"

    with open(fasta_filename) as f:
        lines = f.readlines()

    with open(processed_filename, 'w') as g:
        for line in lines:
            g.write(line.replace(name_prefix, 's'))


