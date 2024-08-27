from pathlib import Path

import pandas as pd

from veptools.modules.logger import Logger
from veptools.modules.mprofile import calculate_profile

LOGGER = Logger(name="pgimpact")


def assign_variables(args):
    inp = pd.read_table(args.input[0], sep="\t")
    out = args.output[0]
    grouping_var = args.grouping_var[0]
    return inp, out, grouping_var, args.verbose


def get_pgimpact_df(inp, grouping_var, verbose):
    pgi_df = {
        "SYMBOL": [],
        grouping_var: [],
        "count": [],
        "count_mean": [],
        "count_sd": [],
    }
    for cat in inp[grouping_var].unique():
        sel = inp[inp[grouping_var] == cat]
        genes = list(sel["SYMBOL"].unique())
        samples = list(sel["sample_name"].unique())
        profile = calculate_profile(sel, genes, samples, False, verbose)
        if verbose:  # pragma: no cover
            LOGGER.info(f"Calculating statistics within group: {cat}")
        pgi_df["SYMBOL"] += genes
        pgi_df[grouping_var] += [cat for _ in range(profile.shape[0])]
        pgi_df["count"] += list(profile.sum(axis=1))
        pgi_df["count_mean"] += list(profile.mean(axis=1))
        pgi_df["count_sd"] += list(profile.std(axis=1))
    pgimpact_df = pd.DataFrame(pgi_df)
    return pgimpact_df


def save_pgimpact(df, out, verbose):
    if verbose:  # pragma: no cover
        LOGGER.info(f"Saving pgimpact table to: {out}")
    Path(out).parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(out, sep="\t", index=False)
