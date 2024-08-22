import argparse
import sys

from veptools.modules import mprofile


class CustomParser(argparse.ArgumentParser):
    def error(self, message):
        sys.stderr.write("error: %s\n" % message)
        self.print_help()
        sys.exit(2)


def run_mprofile(args):
    inp, out, genes, samples, binary = mprofile.assign_variables(args)
    mprofile.checkpoint(inp, samples)
    profile = mprofile.calculate_profile(inp, genes, samples, binary)
    mprofile.save_profile(samples, genes, profile, out)


def get_parser():

    # main parser
    parser = CustomParser(prog="veptools", description="")
    subparsers = parser.add_subparsers(
        title="commands",
    )

    # mprofile
    mprofile_parser = subparsers.add_parser("mprofile", help="")
    mprofile_parser.add_argument(
        "-i",
        metavar="<input>",
        nargs="+",
        help="path to input file(s)",
        required=True,
    )
    mprofile_parser.add_argument(
        "-o",
        metavar="<output>",
        nargs=1,
        help="path to output file",
        required=True,
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

    group = mprofile_parser.add_mutually_exclusive_group(required=False)
    group.add_argument(
        "-s",
        metavar="<sample>",
        nargs="*",
        help="whitespace separated list of sample names",
    )
    group.add_argument(
        "-S",
        metavar="<sample_list_path>",
        nargs=1,
        help="path to sample name list file where each name is in new line",
    )

    mprofile_parser.add_argument(
        "--binary",
        help="wether to calculate a binary profile",
        action="store_true",
    )

    mprofile_parser.set_defaults(func=run_mprofile)

    # compare
    subparsers.add_parser("compare", help="")

    return parser


def cli():
    parser = get_parser()
    args = parser.parse_args()
    try:
        args.func(args)
    except AttributeError:
        parser.print_help(sys.stderr)


if __name__ == "__main__":
    cli()

