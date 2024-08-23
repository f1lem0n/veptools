import argparse
import sys

from veptools.modules import aggregate, mprofile


class CustomParser(argparse.ArgumentParser):
    def error(self, message):
        sys.stderr.write("error: %s\n" % message)
        self.print_help()
        sys.exit(2)


def run_mprofile(args):
    inp, out, genes, samples, binary = mprofile.assign_variables(args)
    profile = mprofile.calculate_profile(inp, genes, samples, binary)
    mprofile.save_profile(genes, samples, profile, out)


def run_aggregate(args):
    inp, out, sample_info = aggregate.assign_variables(args)
    aggregate.checkpoint(inp, sample_info)
    df = aggregate.get_aggregated_df(inp, sample_info)
    df.to_csv(out, index=False, sep="\t")


def get_parser():

    # main parser
    parser = CustomParser(prog="veptools", description="")
    subparsers = parser.add_subparsers(title="commands")

    # aggregate
    aggregate_parser = subparsers.add_parser(
        "aggregate",
        help="aggregate VEP results and sample info into a single table",
    )
    aggregate_parser.add_argument(
        "-i",
        metavar="<input>",
        nargs="+",
        help="path to input file(s)",
        required=True,
    )
    aggregate_parser.add_argument(
        "-o",
        metavar="<output>",
        nargs=1,
        help="path to output file",
        required=True,
    )
    aggregate_parser.add_argument(
        "-s",
        metavar="<sample_info_path>",
        nargs=1,
        help="path to tab separated sample info table",
        required=True,
    )
    aggregate_parser.set_defaults(func=run_aggregate)

    # mprofile
    mprofile_parser = subparsers.add_parser(
        "mprofile", help="calculate mutation profile"
    )
    mprofile_parser.add_argument(
        "-i",
        metavar="<input>",
        nargs="+",
        help="path to input file created via veptools aggregate",
        required=True,
    )
    mprofile_parser.add_argument(
        "-o",
        metavar="<output>",
        nargs=1,
        help="path to output file",
        required=True,
    )
    mprofile_parser.add_argument(
        "--binary",
        help="wether to calculate a binary profile",
        action="store_true",
    )
    group = mprofile_parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "-g",
        metavar="<gene>",
        nargs="+",
        help="whitespace separated list of genes to consider in profile",
    )
    group.add_argument(
        "-G",
        metavar="<gene_list_path>",
        nargs=1,
        help="path to gene list file where each gene is in new line",
    )
    mprofile_parser.set_defaults(func=run_mprofile)

    # pgimpact
    # pgimpact_parser = subparsers.add_parser(
    #    "pgimpact", help="calculate per gene impact",
    # )
    # pgimpact_parser.add_argument(
    #    "-i",
    #    metavar="<input>",
    #    nargs="+",
    #    help="path to input file created via veptools aggregate",
    #    required=True,
    # )

    return parser


def cli():
    parser = get_parser()
    args = parser.parse_args()
    try:
        args.func(args)
    except Exception as e:
        print(e)
        parser.print_help(sys.stderr)


if __name__ == "__main__":
    cli()
