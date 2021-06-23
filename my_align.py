#!/usr/bin/python
# BONUS 9.2 IMPLEMENTED
import os
import sys
from Bio.PDB import *
from Bio import pairwise2
from Bio.Align import MultipleSeqAlignment
from Bio.SeqRecord import SeqRecord
from Bio.Alphabet import IUPAC
from Bio.Seq import Seq


def retrieve_pdb_file(name1):
    """
    Downloads the pdb file according to the input identifier
    """
    pdbl = PDBList()
    return pdbl.retrieve_pdb_file(name1, obsolete=False, pdir=os.getcwd())


def filter_ca_residues(chain):
    """
    Filter the residues containing the C-alpha atoms from a given chain
    """
    ca_list = [atom for atom in chain.get_atoms() if atom.id == "CA"]
    return ca_list


def align(structure, ca_list, ref_ca_list):
    """
    Aligns the 2 atom lists, outputs the RMSE of the alignment
    """
    super_imposer = Superimposer()

    # align the sequences
    super_imposer.set_atoms(ref_ca_list, ca_list)

    # output score (default = RMSE)
    print(super_imposer.rms)

    # apply the transformation to the rest of the atoms
    super_imposer.apply(structure[0].get_atoms())


def align_bonus(structure1, structure2):
    """
    Apply sequence alignment between the two protein structures prior to their structural alignment
    """
    # get aa sequences
    seq1 = get_aa_seq(structure1)
    seq2 = get_aa_seq(structure2)

    # align sequences
    alignments = pairwise2.align.globalxx(seq1, seq2)
    sequence_alignment = MultipleSeqAlignment([SeqRecord(Seq(alignments[0][0], alphabet=IUPAC.protein)),
                                               SeqRecord(Seq(alignments[0][1], alphabet=IUPAC.protein))])
    structure_align = StructureAlignment(sequence_alignment, structure1, structure2)

    # get residues map for the alignment
    map1, map2 = structure_align.get_maps()

    # creates list of CA atoms from the aligned sequence
    ca_l1, ca_l2 = [], []
    for value, key in map2.items():
        if not key:
            continue
        ca_l1.append(value['CA'])
        ca_l2.append(key['CA'])

    # align the corresponding ca atoms
    align(structure1, ca_l1, ca_l2)


def get_aa_seq(structure):
    """
    Returns the amino acid sequence of a given structure
    """
    seq = ''
    ppb = PPBuilder()
    for pp in ppb.build_peptides(structure):
        seq += pp.get_sequence()
    return seq


def save_aligned(structure, pdb_id):
    """
    Saves the alignment in mmCIF format
    """
    io = MMCIFIO()
    io.set_structure(structure)
    io.save(pdb_id + ".cif")


if __name__ == "__main__":
    # check that the argument number is legal
    if len(sys.argv) < 5:
        print("Not enough input arguments, Exiting..")
        exit()

    pdb_id1 = sys.argv[1]
    pdb_id2 = sys.argv[3]
    chain_id1 = sys.argv[2]
    chain_id2 = sys.argv[4]

    # retrieve the relevant pdb files
    path1 = retrieve_pdb_file(pdb_id1)
    path2 = retrieve_pdb_file(pdb_id2)

    # get the structure
    parser = MMCIFParser()
    structure1 = parser.get_structure(pdb_id1, path1)
    structure2 = parser.get_structure(pdb_id2, path2)

    # get the relevant chains
    chain1 = structure1[0][chain_id1]
    chain2 = structure2[0][chain_id2]

    # filter only residues containing C-alpha atoms
    ca_list1 = filter_ca_residues(chain1)
    ca_list2 = filter_ca_residues(chain2)

    # check if the chains have the same number of ca atoms and apply the relevant alignment
    if len(ca_list1) != len(ca_list2):
        print("Different chain lengths, applying sequence alignment before structural alignment (BONUS 9.2)")
        align_bonus(structure1, structure2)
    else:
        # align the sequences,  output score (default = RMSE)
        align(structure1, ca_list1, ca_list2)

    # save the alignment
    save_aligned(structure1, pdb_id1)
