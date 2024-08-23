from pathlib import Path

import numpy as np
import pandas as pd


def assign_variables(args):
    inp = pd.read_table(args.i[0], sep="\t")
    out = args.o[0]
    binary = args.binary
    samples = list(inp["sample_name"].unique())

    if args.g:
        genes = args.g
    else:
        with open(args.G[0]) as f:
            genes = f.read().splitlines()

    return inp, out, genes, samples, binary


def calculate_profile(inp, genes, samples, binary):
    inp = inp[inp["gene_id"].isin(genes) | inp["SYMBOL"].isin(genes)]
    profile = np.zeros((len(genes), len(samples)))
    for sample_idx, sample in enumerate(samples):
        df = inp[inp["sample_name"] == sample]
        for gene_idx, gene in enumerate(genes):
            if gene in list(df["gene_id"]):
                if binary:
                    profile[gene_idx, sample_idx] = 1
                else:
                    profile[gene_idx, sample_idx] = list(df["gene_id"]).count(
                        gene
                    )
            if gene in list(df["SYMBOL"]):
                if binary:
                    profile[gene_idx, sample_idx] = 1
                else:
                    profile[gene_idx, sample_idx] = list(df["SYMBOL"]).count(
                        gene
                    )
            else:
                continue
    profile = profile.astype(int)
    return profile


def save_profile(genes, samples, profile, out):
    profile = pd.DataFrame(
        data=profile,
        columns=samples,
        index=genes,
    )
    Path(out).parent.mkdir(parents=True, exist_ok=True)
    profile.to_csv(out, sep="\t")
