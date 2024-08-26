from pathlib import Path
from statistics import NormalDist

import pandas as pd

from veptools.modules.mprofile import calculate_profile


def assign_variables(args):
    inp = pd.read_table(args.i[0], sep="\t")
    out = args.o[0]
    grouping_var = args.g[0]
    conf_level = args.c[0]
    return inp, out, grouping_var, conf_level


def calculate_ci(arr, conf_level):
    mean = arr.mean(axis=1)
    if arr.shape[1] < 2:
        return mean, mean
    z = NormalDist().inv_cdf((1 + conf_level) / 2.0)
    h = arr.std(axis=1) * z / ((arr.shape[1] - 1) ** 0.5)
    return mean - h, mean + h


def get_pgimpact_df(inp, grouping_var, conf_level):
    pgi_df = {
        "SYMBOL": [],
        grouping_var: [],
        "count": [],
        "count_mean": [],
        "count_sd": [],
        "lower_ci": [],
        "upper_ci": [],
    }
    for cat in inp[grouping_var].unique():
        sel = inp[inp[grouping_var] == cat]
        genes = list(sel["SYMBOL"].unique())
        samples = list(sel["sample_name"].unique())
        profile = calculate_profile(sel, genes, samples, binary=False)
        ci = calculate_ci(profile, conf_level)

        pgi_df["SYMBOL"] += genes
        pgi_df[grouping_var] += [cat for _ in range(profile.shape[0])]
        pgi_df["count"] += list(profile.sum(axis=1))
        pgi_df["count_mean"] += list(profile.mean(axis=1))
        pgi_df["count_sd"] += list(profile.std(axis=1))
        pgi_df["lower_ci"] += list(ci[0])
        pgi_df["upper_ci"] += list(ci[1])
    pgimpact_df = pd.DataFrame(pgi_df)
    return pgimpact_df


def save_pgimpact(df, out):
    Path(out).parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(out, sep="\t", index=False)


#   inp = "tests/data/aggregate_output.tsv"
#   out = "tests/output/pgimpact_output.tsv"
#   grouping_var = "phenotype"
#   conf_level = 0.95
#
#   df = pd.read_table(inp, sep = "\t")
