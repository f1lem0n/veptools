import numpy as np
import pandas as pd
import pytest

from veptools.modules.mprofile import (
    assign_variables,
    calculate_profile,
    checkpoint,
    save_profile,
)
from veptools.veptools import get_parser

parser = get_parser()


def test_assign_variables():

    # -s -g
    args = parser.parse_args(
        [
            "mprofile",
            "-i",
            "tests/data/mprofile_input_A.tsv",
            "tests/data/mprofile_input_B.tsv",
            "-o",
            "tests/output/mprofile_output.csv",
            "-g",
            "ENSG00000254153",
            "ENSG00000228327",
            "ENSG00000291215",
            "ENSG00000131591",
            "-s",
            "A",
            "B",
        ]
    )
    inp, out, genes, samples, binary = assign_variables(args)
    assert inp == [
        "tests/data/mprofile_input_A.tsv",
        "tests/data/mprofile_input_B.tsv",
    ]
    assert out == "tests/output/mprofile_output.csv"
    assert genes == [
        "ENSG00000254153",
        "ENSG00000228327",
        "ENSG00000291215",
        "ENSG00000131591",
    ]
    assert samples == ["A", "B"]
    assert binary is False

    # -S -G
    args = parser.parse_args(
        [
            "mprofile",
            "-i",
            "tests/data/mprofile_input_A.tsv",
            "tests/data/mprofile_input_B.tsv",
            "-o",
            "tests/output/mprofile_output.csv",
            "-G",
            "tests/data/mprofile_genes.txt",
            "-S",
            "tests/data/mprofile_samples.txt",
            "--binary",
        ]
    )
    inp, out, genes, samples, binary = assign_variables(args)
    assert inp == [
        "tests/data/mprofile_input_A.tsv",
        "tests/data/mprofile_input_B.tsv",
    ]
    assert out == "tests/output/mprofile_output.csv"
    assert genes == [
        "ENSG00000254153",
        "ENSG00000228327",
        "ENSG00000291215",
        "ENSG00000131591",
    ]
    assert samples == ["A", "B"]
    assert binary is True

    # no samples
    args = parser.parse_args(
        [
            "mprofile",
            "-i",
            "tests/data/mprofile_input_A.tsv",
            "tests/data/mprofile_input_B.tsv",
            "-o",
            "tests/output/mprofile_output.csv",
            "-G",
            "tests/data/mprofile_genes.txt",
            "--binary",
        ]
    )
    inp, out, genes, samples, binary = assign_variables(args)
    assert inp == [
        "tests/data/mprofile_input_A.tsv",
        "tests/data/mprofile_input_B.tsv",
    ]
    assert out == "tests/output/mprofile_output.csv"
    assert genes == [
        "ENSG00000254153",
        "ENSG00000228327",
        "ENSG00000291215",
        "ENSG00000131591",
    ]
    assert samples == [
        "tests/data/mprofile_input_A.tsv",
        "tests/data/mprofile_input_B.tsv",
    ]
    assert binary is True


def test_checkpoint():
    checkpoint(["file_1", "file_2"], ["sample_1", "sample_2"])
    with pytest.raises(AssertionError):
        checkpoint(["file_1", "file_2"], ["sample_1"])


def test_calculate_profile():

    # binary
    args = parser.parse_args(
        [
            "mprofile",
            "-i",
            "tests/data/mprofile_input_A.tsv",
            "tests/data/mprofile_input_B.tsv",
            "-o",
            "tests/output/mprofile_output.csv",
            "-G",
            "tests/data/mprofile_genes.txt",
            "-S",
            "tests/data/mprofile_samples.txt",
            "--binary",
        ]
    )
    inp, out, genes, samples, binary = assign_variables(args)
    profile = calculate_profile(inp, genes, samples, binary)
    assert (profile == np.array([[0, 0], [1, 1], [1, 1], [0, 1]])).all()

    # count
    args = parser.parse_args(
        [
            "mprofile",
            "-i",
            "tests/data/mprofile_input_A.tsv",
            "tests/data/mprofile_input_B.tsv",
            "-o",
            "tests/output/mprofile_output.csv",
            "-G",
            "tests/data/mprofile_genes.txt",
            "-S",
            "tests/data/mprofile_samples.txt",
        ]
    )
    inp, out, genes, samples, binary = assign_variables(args)
    profile = calculate_profile(inp, genes, samples, binary)
    assert (profile == np.array([[0, 0], [1, 1], [1, 1], [0, 13]])).all()


def test_save_profile():
    args = parser.parse_args(
        [
            "mprofile",
            "-i",
            "tests/data/mprofile_input_A.tsv",
            "tests/data/mprofile_input_B.tsv",
            "-o",
            "tests/output/mprofile_output.csv",
            "-G",
            "tests/data/mprofile_genes.txt",
            "-S",
            "tests/data/mprofile_samples.txt",
        ]
    )
    inp, out, genes, samples, binary = assign_variables(args)
    profile = calculate_profile(inp, genes, samples, binary)
    save_profile(samples, genes, profile, out)
    df = pd.read_csv("tests/output/mprofile_output.csv", index_col=0)
    _df = pd.DataFrame(
        {"A": [0, 1, 1, 0], "B": [0, 1, 1, 13]},
        index=[
            "ENSG00000254153",
            "ENSG00000228327",
            "ENSG00000291215",
            "ENSG00000131591",
        ],
    )
    assert (df.values == _df.values).all()
    assert (df.index == _df.index).all()
    assert (df.columns == _df.columns).all()
