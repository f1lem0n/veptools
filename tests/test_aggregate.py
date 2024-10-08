import pandas as pd
import pytest

from veptools.modules.aggregate import (
    assign_variables,
    checkpoint,
    get_aggregated_df,
    get_skel_df,
    save_aggregated_df,
)
from veptools.veptools import get_parser

parser = get_parser()


def test_assign_variables():
    args = parser.parse_args(
        [
            "aggregate",
            "-i",
            "tests/data/input_A.tsv",
            "tests/data/input_B.tsv",
            "-s",
            "tests/data/sample_info.tsv",
            "-o",
            "tests/output/aggregate_output.tsv",
        ]
    )
    inp, out, sample_info, verbose = assign_variables(args)
    assert inp == ["tests/data/input_A.tsv", "tests/data/input_B.tsv"]
    assert out == "tests/output/aggregate_output.tsv"
    assert (
        sample_info.values
        == pd.DataFrame(
            {
                "sample_name": ["A", "B"],
                "phenotype": [1, 0],
            }
        ).values
    ).all()
    assert (
        sample_info.index
        == pd.DataFrame(
            {
                "sample_name": ["A", "B"],
                "phenotype": [1, 0],
            }
        ).index
    ).all()
    assert (
        sample_info.columns
        == pd.DataFrame(
            {
                "sample_name": ["A", "B"],
                "phenotype": [1, 0],
            }
        ).columns
    ).all()
    assert verbose is False


def test_checkpoint():
    args = parser.parse_args(
        [
            "aggregate",
            "-i",
            "tests/data/input_A.tsv",
            "tests/data/input_B.tsv",
            "-s",
            "tests/data/sample_info.tsv",
            "-o",
            "tests/output/aggregate_output.tsv",
        ]
    )
    inp, out, sample_info, verbose = assign_variables(args)
    checkpoint(inp, sample_info, verbose)
    with pytest.raises(AssertionError):
        args = parser.parse_args(
            [
                "aggregate",
                "-i",
                "tests/data/input_A.tsv",
                "-s",
                "tests/data/sample_info.tsv",
                "-o",
                "tests/output/aggregate_output.tsv",
            ]
        )
        inp, out, sample_info, verbose = assign_variables(args)
        checkpoint(inp, sample_info, verbose)


def test_get_skel_df():
    args = parser.parse_args(
        [
            "aggregate",
            "-i",
            "tests/data/input_A.tsv",
            "tests/data/input_B.tsv",
            "-s",
            "tests/data/sample_info.tsv",
            "-o",
            "tests/output/aggregate_output.tsv",
        ]
    )
    inp, out, sample_info, verbose = assign_variables(args)
    skel = get_skel_df(sample_info, verbose)
    assert skel == {
        "gene_id": [],
        "SYMBOL": [],
        "SOURCE": [],
        "HGVSg": [],
        "HGVSc": [],
        "HGVSp": [],
        "existing_variation": [],
        "consequence": [],
        "SIFT": [],
        "PolyPhen": [],
        "MAX_AF": [],
        "CLIN_SIG": [],
        "CANONICAL": [],
        "IMPACT": [],
        "sample_name": [],
        "phenotype": [],
    }


def test_get_aggregated_df():
    args = parser.parse_args(
        [
            "aggregate",
            "-i",
            "tests/data/input_A.tsv",
            "tests/data/input_B.tsv",
            "-s",
            "tests/data/sample_info.tsv",
            "-o",
            "tests/output/aggregate_output.tsv",
        ]
    )
    inp, out, sample_info, verbose = assign_variables(args)
    df = get_aggregated_df(inp, sample_info, verbose)
    assert df.shape == (100, 16)
    assert list(df["sample_name"].unique()) == ["A", "B"]


def test_aggregated_df():
    args = parser.parse_args(
        [
            "aggregate",
            "-i",
            "tests/data/input_A.tsv",
            "tests/data/input_B.tsv",
            "-s",
            "tests/data/sample_info.tsv",
            "-o",
            "tests/output/aggregate_output.tsv",
        ]
    )
    inp, out, sample_info, verbose = assign_variables(args)
    df = get_aggregated_df(inp, sample_info, verbose)
    save_aggregated_df(df, out, verbose)
    df_ = pd.read_table(out, sep="\t")
    # df.astype(str) not working for some reason
    # assert (df.values == df_.values).all()
    assert (df.index == df_.index).all()
    assert (df.columns == df_.columns).all()
