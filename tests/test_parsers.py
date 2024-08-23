from veptools.veptools import get_parser

parser = get_parser()


def test_aggregate_parser():
    args = parser.parse_args(
        [
            "aggregate",
            "-i",
            "tests/data/input_A.tsv",
            "tests/data/input_B.tsv",
            "-o",
            "tests/output/aggregate_output.csv",
            "-s",
            "tests/data/sample_info.csv",
        ]
    )
    assert args.i == [
        "tests/data/input_A.tsv",
        "tests/data/input_B.tsv",
    ]
    assert args.o == [
        "tests/output/aggregate_output.csv",
    ]


def test_mprofile_parser():

    # -g
    args = parser.parse_args(
        [
            "mprofile",
            "-i",
            "tests/output/aggregate_output.csv",
            "-o",
            "tests/output/mprofile_output.csv",
            "-g",
            "ENSG00000187583",
            "ENSG00000254153",
            "ENSG00000130762",
            "ARHGEF16",
        ]
    )
    assert args.i == [
        "tests/output/aggregate_output.csv",
    ]
    assert args.o == [
        "tests/output/mprofile_output.csv",
    ]
    assert args.g == [
        "ENSG00000187583",
        "ENSG00000254153",
        "ENSG00000130762",
        "ARHGEF16",
    ]
    assert args.G is None
    assert args.binary is False

    # -G
    args = parser.parse_args(
        [
            "mprofile",
            "-i",
            "tests/output/aggregate_output.csv",
            "-o",
            "tests/output/mprofile_output.csv",
            "-G",
            "tests/data/gene_list.txt",
            "--binary",
        ]
    )
    assert args.i == [
        "tests/output/aggregate_output.csv",
    ]
    assert args.o == [
        "tests/output/mprofile_output.csv",
    ]
    assert args.G == ["tests/data/gene_list.txt"]
    assert args.g is None
    assert args.binary is True
