from Bio import AlignIO

CDR_1 = (28, 40)
CDR_2 = (55, 66)
CDR_3 = (107, 117)

align = AlignIO.read("Phylip/interlaced.phy", "phylip")


def get_CDRs():
    return CDR_1, CDR_2, CDR_3
