from Bio import SeqIO
import pickle as pkl


def process_db(fasta_filename, processed_filename, name_prefix):
    """
    Process the DB file in order to present the clustering output appropriately
    :param fasta_filename:
    :param processed_filename:
    :param name_prefix:
    :return:
    """
    with open(fasta_filename) as f:
        lines = f.readlines()

    with open(processed_filename, 'w') as g:
        for line in lines:
            g.write(line.replace(name_prefix, 's'))


def build_name_seq_dict(processed_filename):
    """
    build a name sequence dictionary
    :param processed_filename: Fasta file
    :return: name sequence dictionary
    """
    name_seq_dict = {}
    for seq_record in SeqIO.parse(processed_filename, "fasta"):
        name_seq_dict[seq_record.name] = str(seq_record.seq)
    return name_seq_dict


def process_clustering(processed_filename, cluster_filename, output_name):
    """
    Creates the clustering sequences data
    :param processed_filename: DB filename
    :param cluster_filename: clustering filename
    :param output_name: name to save the dict as pickle object
    :return:
    """
    with open(cluster_filename) as f:
        lines = f.readlines()

    seq_clusters = {}
    name_clusters = {}
    name = None
    members = []

    for line in lines:
        if line.startswith(">"):
            if name is not None:
                #store only clusters with more than one sequence
                if len(members) > 0:
                    name_clusters[name] = members
                name = None
                members = []
        else:
            if line.endswith('*\n'):
                name = line.split('>')[1].split('.')[0]
            elif line.endswith('%\n'):
                members.append(line.split('>')[1].split('.')[0])

    if name is not None:
        if len(members) > 0:
            name_clusters[name] = members

    print(name_clusters)

    name_seq_dict = build_name_seq_dict(processed_filename)

    for key in name_clusters:
        members = name_clusters[key]
        key_seq = name_seq_dict[key]
        members_seq = [name_seq_dict[f] for f in members]
        seq_clusters[key_seq] = members_seq

    print(seq_clusters)
    with open(output_name, 'wb') as handle:
        pkl.dump(seq_clusters, handle)


if __name__ == '__main__':
    fasta_filename = "AboutMillionSequencesNew.fasta"
    processed_filename = "AboutMillionSequencesProcessed.fasta"
    name_prefix = "7168_4th_CoV2_BL"
    cluster_filename = "Data/out.clstr"
    output_clustering = "output_clustering.pkl"
    # process_db(fasta_filename, processed_filename, name_prefix)
    process_clustering(processed_filename, cluster_filename, output_clustering)

