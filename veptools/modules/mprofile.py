from pathlib import Path

import numpy as np
import pandas as pd

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
    "extra",
]


def assign_variables(args):
    inp = args.i
    out = args.o[0]
    binary = args.binary

    if args.g:
        genes = args.g
    else:
        with open(args.G[0]) as f:
            genes = f.read().splitlines()

    if args.s:
        samples = args.s
    elif args.S:
        with open(args.S[0]) as f:
            samples = f.read().splitlines()
    else:
        samples = inp

    return inp, out, genes, samples, binary


def checkpoint(inp, samples):
    assert len(inp) == len(samples), \
    "Number of samples must be equal to the number of input files"


def calculate_profile(inp, genes, samples, binary):
    profile = np.zeros((len(genes), len(samples)))
    for sample_idx, filepath in enumerate(inp):
        df = pd.read_table(filepath, sep="\t", names=COLNAMES)
        df = df[df["gene"].isin(genes)]
        for gene in df["gene"].values:
            if binary:
                profile[genes.index(gene), sample_idx] = 1
            else:
                profile[genes.index(gene), sample_idx] += 1

    return profile


def save_profile(samples, genes, profile, out):
    profile = pd.DataFrame(
        data=profile,
        columns=samples,
        index=genes,
    )
    profile = profile.astype(int)
    Path(out).parent.mkdir(parents=True, exist_ok=True)
    profile.to_csv(out)
