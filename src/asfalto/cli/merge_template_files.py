from asfalto.template.merge import merge


def register(subparsers):
    parser = subparsers.add_parser(
        "merge",
        help="subcommand for merging the intermediate files created during template generation.",
    )

    parser.add_argument(
        "input",
        help="the path to the working directory with the intermediate files to be merged. Requires at least two turtle files with the same name appended with '-declarations' and '-expanded'.",
        metavar="working_directory",
    )

    parser.add_argument(
        "--include-refs",
        "-i",
        help="set whether to add information of given terms from the references folder. This will apply an SLME-BOT algorithm to extract only relevant terms.",
        action="store_true",
    )

    parser.set_defaults(_handler=run)


def run(args):
    print(f"merging files in working directory {args.input}...")
    merge(args.input, include_refs=args.include_refs)
