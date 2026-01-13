from asfalto.populate.normalize import normalize_graph


def register(subparsers):
    parser = subparsers.add_parser(
        "normalize",
        help="subcommand to process an rdf file and expand templated terms and traits.",
    )

    parser.add_argument(
        "input_path",
        help="the path to the input ontology file or drawio diagram. Inputs in the turtle formats are strongly recommended.",
        metavar="input_file_path",
    )

    parser.add_argument(
        "template_folder",
        help="the path(s) to the folder containing the templates. Separate multiple paths with commas only. e.g. ../templates,../detector-result",
        metavar="template_folder",
    )

    parser.add_argument(
        "--output-path",
        "-o",
        help="a custom path for outputting the normalized ontology. If no input is given, the input will be modified in-place.",
        metavar="output_path",
        default=None,
    )

    parser.set_defaults(_handler=run)


def run(args):
    normalize_graph(args.input_path, args.template_folder, output_path=args.output_path)
