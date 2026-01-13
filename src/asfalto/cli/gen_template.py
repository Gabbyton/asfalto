from asfalto.template.generate_template import generate_template


def register(subparsers):
    parser = subparsers.add_parser(
        "template",
        help="subcommand for generating a stottr and csv template for the given template draw.io drawing",
    )

    parser.add_argument(
        "input",
        help="the path to the draw.io file containing the template terms.",
        metavar="input_drawio_file",
    )

    parser.add_argument(
        "output",
        help="the path to the folder where the program outputs will be generated.",
        metavar="output_folder",
    )

    parser.add_argument(
        "-n",
        "--name",
        help="the name to assign to the template variable itself (including the prefix). i.e. ex:Motor",
        metavar="template_varname",
        default=None,
    )

    parser.add_argument(
        "-p",
        "--prefix",
        help="the default prefix to assign to the template variable name if no name is provided.",
        metavar="template_var_prefix",
        default="mds",
    )

    parser.add_argument(
        "-excel",
        "--use-excel",
        help="set whether to produce an excel file for the manual template input sheet.",
        action="store_true",
    )

    parser.set_defaults(_handler=run)


def run(args):
    print(f"converting {args.input} into a csv template at {args.output}...")
    generate_template(
        input_path=args.input,
        output_folder=args.output,
        template_name=args.name,
        default_prefix=args.prefix,
        export_excel=args.use_excel,
    )
