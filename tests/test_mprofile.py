import numpy as np
import pandas as pd

from veptools.modules.mprofile import (
    assign_variables,
    calculate_profile,
    save_profile,
)
from veptools.veptools import get_parser

parser = get_parser()


def test_assign_variables():

    # -g
    args = parser.parse_args(
        [
            "mprofile",
            "-i",
            "tests/data/aggregate_output.csv",
            "-o",
            "tests/output/mprofile_output.csv",
            "-g",
            "ENSG00000187583",
            "ENSG00000254153",
            "ENSG00000130762",
            "ARHGEF16",
        ]
    )
    inp, out, genes, samples, binary = assign_variables(args)
    assert inp.shape == (100, 16)
    assert out == "tests/output/mprofile_output.csv"
    assert genes == [
        "ENSG00000187583",
        "ENSG00000254153",
        "ENSG00000130762",
        "ARHGEF16",
    ]
    assert samples == ["A", "B"]
    assert binary is False

    # -G
    args = parser.parse_args(
        [
            "mprofile",
            "-i",
            "tests/data/aggregate_output.csv",
            "-o",
            "tests/output/mprofile_output.csv",
            "-G",
            "tests/data/gene_list.txt",
            "--binary",
        ]
    )
    inp, out, genes, samples, binary = assign_variables(args)
    assert inp.shape == (100, 16)
    assert out == "tests/output/mprofile_output.csv"
    assert genes == [
        "ENSG00000187583",
        "ENSG00000254153",
        "ENSG00000130762",
        "ARHGEF16",
    ]
    assert samples == ["A", "B"]
    assert binary is True


def test_calculate_profile():

    # binary
    args = parser.parse_args(
        [
            "mprofile",
            "-i",
            "tests/data/aggregate_output.csv",
            "-o",
            "tests/output/mprofile_output.csv",
            "-G",
            "tests/data/gene_list.txt",
            "--binary",
        ]
    )
    inp, out, genes, samples, binary = assign_variables(args)
    profile = calculate_profile(inp, genes, samples, binary)
    assert (profile == np.array([[1, 0], [0, 0], [0, 1], [0, 1]])).all()

    # count
    args = parser.parse_args(
        [
            "mprofile",
            "-i",
            "tests/data/aggregate_output.csv",
            "-o",
            "tests/output/mprofile_output.csv",
            "-G",
            "tests/data/gene_list.txt",
        ]
    )
    inp, out, genes, samples, binary = assign_variables(args)
    profile = calculate_profile(inp, genes, samples, binary)
    assert (profile == np.array([[3, 0], [0, 0], [0, 5], [0, 7]])).all()


def test_save_profile():
    args = parser.parse_args(
        [
            "mprofile",
            "-i",
            "tests/data/aggregate_output.csv",
            "-o",
            "tests/output/mprofile_output.csv",
            "-G",
            "tests/data/gene_list.txt",
        ]
    )
    inp, out, genes, samples, binary = assign_variables(args)
    profile = calculate_profile(inp, genes, samples, binary)
    save_profile(genes, samples, profile, out)
    df = pd.read_csv("tests/output/mprofile_output.csv", index_col=0)
    _df = pd.DataFrame(
        {"A": [3, 0, 0, 0], "B": [0, 0, 5, 7]},
        index=[
            "ENSG00000187583",
            "ENSG00000254153",
            "ENSG00000130762",
            "ARHGEF16",
        ],
    )
    assert (df.values == _df.values).all()
    assert (df.index == _df.index).all()
    assert (df.columns == _df.columns).all()
