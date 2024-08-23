import pandas as pd

COLNAMES = [
    "uploaded_variation",
    "location",
    "allele",
    "gene_id",
    "feature",
    "feature_type",
    "consequence",
    "cDNA_pos",
    "CDS_pos",
    "protein_pos",
    "amino_acids",
    "codons",
    "existing_variation",
    "extra",
]

DESIRED_COLS = [
    "gene_id",
    "SYMBOL",
    "SOURCE",
    "HGVSg",
    "HGVSc",
    "HGVSp",
    "existing_variation",
    "consequence",
    "SIFT",
    "PolyPhen",
    "MAX_AF",
    "CLIN_SIG",
    "CANONICAL",
    "IMPACT",
]


def assign_variables(args):
    inp = args.i
    out = args.o[0]

    with open(args.s[0]) as f:
        sample_info = pd.read_csv(f, sep="\t", header=0)

    return inp, out, sample_info


def checkpoint(inp, sample_info):
    assert len(inp) == sample_info.shape[0], "Number of files must be equal to"
    " the number of lines in sample info file"


def get_skel_df(sample_info):
    skel = {key: [] for key in DESIRED_COLS}
    for col in sample_info.columns:
        skel[col] = []
    return skel


def get_aggregated_df(inp, sample_info):
    skel = get_skel_df(sample_info)

    for info, file in zip(sample_info.iterrows(), inp):
        df = pd.read_table(file, sep="\t", names=COLNAMES)
        for _, row in df.iterrows():
            extra = row["extra"].split(";")
            extra = {elem.split("=")[0]: elem.split("=")[1] for elem in extra}
            for col in skel.keys():
                if col in df.columns:
                    skel[col].append(row[col])
                elif col in sample_info.columns:
                    skel[col].append(info[1][col])
                elif col in extra:
                    skel[col].append(extra[col])
                else:
                    skel[col].append("-")

    df = pd.DataFrame(skel)
    return df
