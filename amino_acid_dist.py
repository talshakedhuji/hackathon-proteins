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

print(sum(AMINO_ACID_DIST.values()))