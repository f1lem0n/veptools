from pathlib import Path

import pandas as pd

from veptools.modules.mprofile import calculate_profile


def assign_variables(args):
    inp = pd.read_table(args.i[0], sep="\t")
    out = args.o[0]
    grouping_var = args.g[0]
    return inp, out, grouping_var


def get_pgimpact_df(inp, grouping_var):
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
        profile = calculate_profile(sel, genes, samples, binary=False)

        pgi_df["SYMBOL"] += genes
        pgi_df[grouping_var] += [cat for _ in range(profile.shape[0])]
        pgi_df["count"] += list(profile.sum(axis=1))
        pgi_df["count_mean"] += list(profile.mean(axis=1))
        pgi_df["count_sd"] += list(profile.std(axis=1))
    pgimpact_df = pd.DataFrame(pgi_df)
    return pgimpact_df


def save_pgimpact(df, out):
    Path(out).parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(out, sep="\t", index=False)
