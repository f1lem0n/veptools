from pathlib import Path

import numpy as np
import pandas as pd

from veptools.modules.logger import Logger

LOGGER = Logger(name="mprofile")


def assign_variables(args):
    inp = pd.read_table(args.input[0], sep="\t")
    out = args.output[0]
    binary = args.binary
    samples = list(inp["sample_name"].unique())

    if args.genes:
        genes = args.genes
    else:
        with open(args.gene_list[0]) as f:
            genes = f.read().splitlines()

    return inp, out, genes, samples, binary, args.verbose


def calculate_profile(inp, genes, samples, binary, verbose):
    inp = inp[inp["gene_id"].isin(genes) | inp["SYMBOL"].isin(genes)]
    profile = np.zeros((len(genes), len(samples)))
    if verbose:  # pragma: no cover
        LOGGER.info(f"Binary mode enabled: {binary}")
    for sample_idx, sample in enumerate(samples):
        if verbose:  # pragma: no cover
            LOGGER.debug(f"Calculating mutation profile for sample: {sample}")
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


def save_profile(genes, samples, profile, out, verbose):
    if verbose:  # pragma: no cover
        LOGGER.info(f"Saving mutation profile to: {out}")
    profile = pd.DataFrame(
        data=profile,
        columns=samples,
        index=genes,
    )
    Path(out).parent.mkdir(parents=True, exist_ok=True)
    profile.to_csv(out, sep="\t")
