from pathlib import Path

import pandas as pd
import numpy as np

COLNAMES = [
    "uploaded_variation",
    "location",
    "allele",
    "gene",
    "feature",
    "feature_type",
    "consequence",
    "cDNA_pos",
    "CDS_pos",
    "protein_pos",
    "amino_acids",
    "codons",
    "existing_variation",
    "extra"
]

def checkpoint(args):
    if args.s:
        assert len(args.i) == len(args.s), \
        "Number of samples must be equal to number of input files"

def calculate_profile(args):
    if not args.s:
        args.s = args.i
    profile = np.zeros((len(args.g), len(args.s)))
    for sample_idx, filepath in enumerate(args.i):
        df = pd.read_table(filepath, sep = "\t", names = COLNAMES)
        df = df[df["gene"].isin(args.g)]
        for gene in df["gene"].values:
            profile[args.g.index(gene), sample_idx] += 1
    return profile

def save_profile(args, profile):
    profile = pd.DataFrame(
        data=profile,
        columns=args.s,
        index=args.g,
    )
    profile.to_csv(args.o[0])
