import argparse
import traceback
import sys

from rich import print

from veptools.modules import aggregate, mprofile, pgimpact


class CustomParser(argparse.ArgumentParser):  # pragma: no cover
    def error(self, message):
        print(f"\n[bold red]error: {message}[/bold red]\n")
        self.print_help()
        sys.exit(2)


def run_mprofile(args):  # pragma: no cover
    inp, out, genes, samples, binary = mprofile.assign_variables(args)
    profile = mprofile.calculate_profile(inp, genes, samples, binary)
    mprofile.save_profile(genes, samples, profile, out)


def run_aggregate(args):  # pragma: no cover
    inp, out, sample_info = aggregate.assign_variables(args)
    aggregate.checkpoint(inp, sample_info)
    df = aggregate.get_aggregated_df(inp, sample_info)
    aggregate.save_aggregated_df(df, out)


def run_pgimpact(args):  # pragma: no cover
    inp, out, grouping_var = pgimpact.assign_variables(args)
    df = pgimpact.get_pgimpact_df(inp, grouping_var)
    pgimpact.save_pgimpact(df, out)


def get_parser():

    # main parser
    parser = CustomParser(prog="veptools", description="")
    parser.add_argument(
        "-v",
        help="enable verbosity",
        action="store_true",
    )
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
    mprofile_parser.add_argument(
        "--binary",
        help="wether to calculate a binary profile",
        action="store_true",
    )
    mprofile_parser.set_defaults(func=run_mprofile)

    # pgimpact
    pgimpact_parser = subparsers.add_parser(
        "pgimpact",
        help="calculate per gene impact",
    )
    pgimpact_parser.add_argument(
        "-i",
        metavar="<input>",
        nargs=1,
        help="path to input file created via veptools aggregate",
        required=True,
    )
    pgimpact_parser.add_argument(
        "-o",
        metavar="<input>",
        nargs=1,
        help="path to output file",
        required=True,
    )
    pgimpact_parser.add_argument(
        "-g",
        metavar="<input>",
        nargs=1,
        help="grouping variable present in aggregated table",
        required=True,
    )
    pgimpact_parser.set_defaults(func=run_pgimpact)

    return parser


def cli():  # pragma: no cover
    parser = get_parser()
    args = parser.parse_args()
    try:
        args.func(args)
    except Exception as message:
        if args.v == True:
            print(traceback.format_exc())
        print(f"\n[bold red]error: {message}[/bold red]\n")
        parser.print_help(sys.stderr)


if __name__ == "__main__":  # pragma: no cover
    cli()
