from collections import Counter, defaultdict
import os
import time

import numpy as np
import pandas as pd
from scipy import stats
import pysam

CLIP_BAM_PATH = '../data/binfo1-datapack1/CLIP-35L33G.bam'
FASTA_DIR_PATH    = '../data/chromFa'
HEXAMER_FASTA_PATH = '../stats/hexamers.fasta'

# Make dctFastaMatch that has {gencode chromID : RefSeq chromID}
lstRefSeqFa = os.listdir(FASTA_DIR_PATH)
dctFastaMatch = {}
for fa in lstRefSeqFa:
    chrId = fa.replace('.fa', '')
    if '_' not in fa:
        dctFastaMatch[chrId] = fa
    else:
        dctFastaMatch[chrId.split('_')[1].replace('v', '.')] = fa
        
del dctFastaMatch['chrM']

DEPTH_CUTOFF = 50
CRES_CUTOFF  = 1.2

def get_chr_binding_positions(chrId):
    pileUp = pysam.AlignmentFile(CLIP_BAM_PATH).pileup(chrId)
    lstBindingPositionsPos, lstBindingPositionsNeg = [], []
    for col in pileUp:
        bases = col.get_query_sequences()
        basesPos = [base for base in bases if base.isupper()]
        basesNeg = [base for base in bases if base.islower()]
        if len(basesPos) >= DEPTH_CUTOFF:
            cres = stats.entropy(list(Counter(bases).values()), base=2)
            if cres >= CRES_CUTOFF:
                lstBindingPositionsPos.append(col.reference_pos)
        if len(basesNeg) >= DEPTH_CUTOFF:
            cres = stats.entropy(list(Counter(bases).values()), base=2)
            if cres >= CRES_CUTOFF:
                lstBindingPositionsNeg.append(col.reference_pos)
    return lstBindingPositionsPos, lstBindingPositionsNeg

# Complement: A <--> T, G <--> C
# Dictionary for the Unicode code point
dctComplement = str.maketrans('ACGT', 'TGCA')

def get_binding_sequences(chrId):
    lstBindingPositionsPos, lstBindingPositionsNeg = get_chr_binding_positions(chrId)

    fasta_file_path = os.path.join(FASTA_DIR_PATH, dctFastaMatch[chrId])
    with open(fasta_file_path, 'rt') as fIn:
        assert next(fIn).startswith('>') # Skip header
        seq = fIn.read().strip().replace('\n', '').upper() # Remove new line chr and make lowercase be uppercase

    dctSeqs = Counter()
    for pos in lstBindingPositionsPos:
        dctSeqs.update([seq[pos-2:pos+4]])
    for pos in lstBindingPositionsNeg:
        hexamer = seq[pos-3:pos+3][::-1].translate(dctComplement)
        dctSeqs.update([hexamer])
    return dctSeqs

dctSeqs = Counter()
for chrId, fa in dctFastaMatch.items():
    print(time.ctime(), f'{fa} now opens', sep=' --- ')
    dctSeqs.update(get_binding_sequences(chrId))

dfHexamers = pd.DataFrame(dctSeqs.most_common(), columns=['hexamer', 'counts']).set_index('hexamer')

dfHexamers.to_csv('../stats/hexamers-cres12.txt', sep='\t')