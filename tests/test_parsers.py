from veptools.veptools import get_parser

def test_mprofile_parser():
    parser = get_parser()

    # -s -g 
    args = parser.parse_args(
        [
            "mprofile",
            "-i", "tests/data/mprofile_input_A.tsv", "tests/data/mprofile_input_B.tsv",
            "-o", "tests/output/mprofile_output.csv",
            "-g", "ENSG00000254153", "ENSG00000228327", "ENSG00000291215", "ENSG00000131591",
            "-s", "A", "B",
        ]
    )
    assert args.i == [
        "tests/data/mprofile_input_A.tsv",
        "tests/data/mprofile_input_B.tsv",
    ]
    assert args.o == [
        "tests/output/mprofile_output.csv",
    ]
    assert args.g == [
        "ENSG00000254153",
        "ENSG00000228327",
        "ENSG00000291215",
        "ENSG00000131591",
    ]
    assert args.s == ["A", "B"]
    assert args.G is None
    assert args.S is None
    assert args.binary is False

    # -S -G
    args = parser.parse_args(
        [
            "mprofile",
            "-i", "tests/data/mprofile_input_A.tsv", "tests/data/mprofile_input_B.tsv",
            "-o", "tests/output/mprofile_output.csv",
            "-G", "tests/data/mprofile_genes.txt",
            "-S", "tests/data/mprofile_samples.txt",
            "--binary"
        ]
    )
    assert args.i == [
        "tests/data/mprofile_input_A.tsv",
        "tests/data/mprofile_input_B.tsv",
    ]
    assert args.o == [
        "tests/output/mprofile_output.csv",
    ]
    assert args.G == [
        "tests/data/mprofile_genes.txt"
    ]
    assert args.S == [
        "tests/data/mprofile_samples.txt"
    ]
    assert args.g is None
    assert args.s is None
    assert args.binary is True

    # no samples
    args = parser.parse_args(
        [
            "mprofile",
            "-i", "tests/data/mprofile_input_A.tsv", "tests/data/mprofile_input_B.tsv",
            "-o", "tests/output/mprofile_output.csv",
            "-G", "tests/data/mprofile_genes.txt",
            "--binary"
        ]
    )
    assert args.i == [
        "tests/data/mprofile_input_A.tsv",
        "tests/data/mprofile_input_B.tsv",
    ]
    assert args.o == [
        "tests/output/mprofile_output.csv",
    ]
    assert args.G == [
        "tests/data/mprofile_genes.txt"
    ]
    assert args.g is None
    assert args.s is None
    assert args.S is None
    assert args.binary is True

