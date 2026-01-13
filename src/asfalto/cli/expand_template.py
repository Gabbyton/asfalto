from asfalto.template.expand import expand_template


def register(subparsers):
    parser = subparsers.add_parser(
        "expand",
        help="subcommand for expanding a generated template sheet into a proper turtle file.",
    )

    parser.add_argument(
        "input",
        help="the path to the sheet containing the populated template terms.",
        metavar="input_sheet_file",
    )

    parser.add_argument(
        "-o",
        "--output-path",
        help="the full path to the desired output file. Defaults to the working directory of the input.",
        metavar="output_file_path",
    )

    parser.add_argument(
        "-t",
        "--template",
        help="the path to the template file to use for expansion. Defaults to the annotated '-template.stottr' file in the working directory of the input.",
        metavar="template_file_path",
        default=None,
    )

    parser.add_argument(
        "-s",
        "--strict",
        help="set whether to remove all unfilled entries versus renaming them with the head node name.",
        default="store_true",
    )

    parser.add_argument(
        "-p",
        "--prefix",
        help="the default prefix to assign to terms with no explicit prefix declarations.",
        metavar="template_var_prefix",
        default="mds",
    )

    parser.add_argument(
        "-db",
        "--write-debug",
        help="Set whether or not to save the intermediate instances stottr file. If set to true, the file will be saved in the working directory of the input.",
        action="store_true",
    )

    parser.set_defaults(_handler=run)


def run(args):
    print(
        f"populating {args.output_path if args.output_path else 'turtle file'} with terms provided in {args.input}..."
    )
    expand_template(
        sheet_instance_file_path=args.input,
        template_file_path=args.template,
        output_file_path=args.output_path,
        strict_mode=args.strict,
        default_prefix=args.prefix,
        write_debug_file=args.write_debug,
    )
