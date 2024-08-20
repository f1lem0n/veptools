from pathlib import Path
import argparse
import sys

from modules import mprofile

class CustomParser(argparse.ArgumentParser):
    def error(self, message):
        sys.stderr.write('error: %s\n' % message)
        self.print_help()
        sys.exit(2)


def run_mprofile(args):
    mprofile.checkpoint(args)
    profile = mprofile.calculate_profile(args)
    mprofile.save_profile(args, profile)


def get_parser():

    # main parser
    parser = CustomParser(
        prog="veptools",
        description=""
    )
    subparsers = parser.add_subparsers(
        title="commands",
    )


    # mprofile
    mprofile_parser = subparsers.add_parser(
        "mprofile",
        help=""
    )
    mprofile_parser.add_argument(
        "-i",
        metavar="<input>",
        nargs="+",
        help="",
        required=True,
    )
    mprofile_parser.add_argument(
        "-o",
        metavar="<output>",
        nargs=1,
        help="",
        required=True,
    )

    group = mprofile_parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "-g",
        metavar="<gene>",
        nargs="+",
        help="",
    )
    group.add_argument(
        "-G",
        metavar="<gene_list_path>",
        nargs=1,
        help=""
    )

    group = mprofile_parser.add_mutually_exclusive_group(required=False)
    group.add_argument(
        "-s",
        metavar="<sample>",
        nargs="*",
        help="",
    )
    group.add_argument(
        "-S",
        metavar="<sample_list_path>",
        nargs=1,
        help="",
    )

    mprofile_parser.set_defaults(func=run_mprofile)


    # compare
    subparsers.add_parser(
        "compare",
        help=""
    )

    return parser


if __name__ == "__main__":
    parser = get_parser()
    args = parser.parse_args()
    try:
        args.func(args)
    except AttributeError:
        parser.print_help(sys.stderr)

