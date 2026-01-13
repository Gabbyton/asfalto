import argparse
import sys

import asfalto.cli.gen_template as gen_temp
import asfalto.cli.expand_template as exp_temp
import asfalto.cli.merge_template_files as merge_files
from asfalto.cli.constants import header
import asfalto.cli.verify as verify
import asfalto.cli.normalize as normalize


def main():
    parser = argparse.ArgumentParser(
        prog="asfalto",
        description=header,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    subparsers = parser.add_subparsers(
        dest="asfalto", metavar="subcommand", title="Available functions", required=True
    )
    subparsers.required = True

    gen_temp.register(subparsers)
    exp_temp.register(subparsers)
    merge_files.register(subparsers)
    verify.register(subparsers)
    normalize.register(subparsers)

    if len(sys.argv) <= 1:
        parser.print_help()
        sys.exit(1)

    args = parser.parse_args()

    if hasattr(args, "_handler"):
        args._handler(args)


if __name__ == "__main__":
    main()
