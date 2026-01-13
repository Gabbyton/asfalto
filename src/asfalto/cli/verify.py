from asfalto.verify.verify import verify_template


def register(subparsers):
    parser = subparsers.add_parser(
        "verify",
        help="subcommand to check for inconsistencies in the input ontology model. Can be drawio diagram or rdf format.",
    )

    parser.add_argument(
        "input",
        help="the path to the input ontology file or drawio diagram. Inputs in the turtle formats are strongly recommended.",
        metavar="input_file_path",
    )

    parser.add_argument(
        "--output-path",
        "-o",
        help="the path to output the inconsistency results.",
        metavar="reasoning_output",
        default=None,
    )

    parser.add_argument(
        "-lsp",
        "--log-substitution-path",
        help="the path to a file that debugs the substitution output.",
        metavar="reasoning_output",
    )

    parser.set_defaults(_handler=run)


def run(args):
    verify_template(
        args.input,
        reason_output_path=args.output_path,
        substitution_debug_path=args.log_substitution_path,
    )
