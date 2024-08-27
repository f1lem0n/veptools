import pandas as pd

from veptools.modules.pgimpact import (
    assign_variables,
    get_pgimpact_df,
    save_pgimpact,
)
from veptools.veptools import get_parser

parser = get_parser()


def test_assign_variables():
    args = parser.parse_args(
        [
            "pgimpact",
            "-i",
            "tests/data/aggregate_output.tsv",
            "-o",
            "tests/output/pgimpact_output.tsv",
            "-g",
            "phenotype",
        ]
    )
    inp, out, grouping_var = assign_variables(args)
    assert inp.shape == (100, 16)
    assert out == "tests/output/pgimpact_output.tsv"
    assert grouping_var == "phenotype"


def test_get_pgimpact_df():
    args = parser.parse_args(
        [
            "pgimpact",
            "-i",
            "tests/data/aggregate_output.tsv",
            "-o",
            "tests/output/pgimpact_output.tsv",
            "-g",
            "phenotype",
        ]
    )
    inp, out, grouping_var = assign_variables(args)
    pgimpact_df = get_pgimpact_df(inp, grouping_var)
    assert (
        pgimpact_df.columns
        == [
            "SYMBOL",
            "phenotype",
            "count",
            "count_mean",
            "count_sd",
        ]
    ).all()
    assert pgimpact_df["SYMBOL"].iloc[0] == "PLEKHN1"
    assert pgimpact_df["count"].iloc[5] == 13
    assert pgimpact_df["count_mean"].iloc[0] == 7.0
    assert pgimpact_df["count_sd"].iloc[15] == 0.0


def test_save_pgimpact():
    args = parser.parse_args(
        [
            "pgimpact",
            "-i",
            "tests/data/aggregate_output.tsv",
            "-o",
            "tests/output/pgimpact_output.tsv",
            "-g",
            "phenotype",
        ]
    )
    inp, out, grouping_var = assign_variables(args)
    pgimpact_df = get_pgimpact_df(inp, grouping_var)
    save_pgimpact(pgimpact_df, out)
    df = pd.read_table(out, sep="\t")
    assert (pgimpact_df.index == df.index).all()
    assert (pgimpact_df.columns == df.columns).all()
    assert (pgimpact_df.values == df.values).all()
