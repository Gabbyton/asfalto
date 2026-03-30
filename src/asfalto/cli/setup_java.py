from asfalto.imports.java import download_jre

def register(subparsers):
    parser = subparsers.add_parser(
        "setup_java",
        help="subcommand to download a pre-built JRE if java is not installed on the system.",
    )

    parser.add_argument(
        "-f",
        "--force",
        help="set whether to force download of the JRE regardless if already cached.",
        default="store_true",
    )

    parser.set_defaults(_handler=run)


def run(args):
    print("Attempting to download JRE from Adoptium...")
    download_jre(force=args.force)
