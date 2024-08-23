import pandas as pd
import pytest

from veptools.modules.aggregate import (
    assign_variables,
    checkpoint,
    get_aggregated_df,
    get_skel_df,
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
            "tests/data/sample_info.csv",
            "-o",
            "tests/output/aggregate_output.csv",
        ]
    )
    inp, out, sample_info = assign_variables(args)
    assert inp == ["tests/data/input_A.tsv", "tests/data/input_B.tsv"]
    assert out == "tests/output/aggregate_output.csv"
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


def test_checkpoint():
    args = parser.parse_args(
        [
            "aggregate",
            "-i",
            "tests/data/input_A.tsv",
            "tests/data/input_B.tsv",
            "-s",
            "tests/data/sample_info.csv",
            "-o",
            "tests/output/aggregate_output.csv",
        ]
    )
    inp, out, sample_info = assign_variables(args)
    checkpoint(inp, sample_info)
    with pytest.raises(AssertionError):
        args = parser.parse_args(
            [
                "aggregate",
                "-i",
                "tests/data/input_A.tsv",
                "-s",
                "tests/data/sample_info.csv",
                "-o",
                "tests/output/aggregate_output.csv",
            ]
        )
        inp, out, sample_info = assign_variables(args)
        checkpoint(inp, sample_info)


def test_get_skel_df():
    args = parser.parse_args(
        [
            "aggregate",
            "-i",
            "tests/data/input_A.tsv",
            "tests/data/input_B.tsv",
            "-s",
            "tests/data/sample_info.csv",
            "-o",
            "tests/output/aggregate_output.csv",
        ]
    )
    inp, out, sample_info = assign_variables(args)
    skel = get_skel_df(sample_info)
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
            "tests/data/sample_info.csv",
            "-o",
            "tests/output/aggregate_output.csv",
        ]
    )
    inp, out, sample_info = assign_variables(args)
    df = get_aggregated_df(inp, sample_info)
    assert df.shape == (100, 16)
