import csv
import io
import re
import shutil
import subprocess
import sys
from pathlib import Path
from tempfile import NamedTemporaryFile

import pandas as pd
from rdflib import Graph, URIRef, RDF
from rdflib.namespace import split_uri

from asfalto.template.constants import IRI_VALUE
from asfalto.template.io import get_default_prefixes
from asfalto.imports.java import get_lutra_path
from asfalto.template.preprocessing import (
    get_prefix_ttl_file_str,
    get_abbrev_term_from_str,
)
from asfalto.template.transforms import get_search_keys, get_best_match


def rename_col_value(
    value: str, template_term: str, head_term: str, default_prefix="mds"
) -> str:
    new_term = str(value).replace(template_term, head_term)
    new_term = f"{default_prefix}:{new_term}"
    return new_term.replace(" ", "")


def replace_string_prefix(prefixes: dict[str, str], term: str) -> str:
    prefix, abbrev = term.split(":")
    return f"{prefixes[prefix.strip()]}{abbrev}"


def expand_template(
    sheet_instance_file_path: str | Path,
    template_file_path: str | Path = None,
    output_file_path: str | Path = None,
    strict_mode: bool = False,
    default_prefix: str = "mds",
    write_debug_file: bool = False,
):
    sheet_instance_file_path = Path(sheet_instance_file_path)
    if sheet_instance_file_path.is_dir():
        sheet_instance_file_path = next(
            sheet_instance_file_path.glob("*-template_sheet*"), None
        )
        if sheet_instance_file_path is None:
            raise ValueError(
                "The given folder does not contain a template sheet. Please make sure to name the file with the '-template_sheet' suffix."
            )

    if output_file_path is None:
        output_file_path = sheet_instance_file_path.with_name(
            f"{sheet_instance_file_path.stem.replace('-template_sheet', '-expanded')}.ttl"
        )

    prefixes = get_default_prefixes()
    inv_prefixes = {value: key for key, value in prefixes.items()}
    default_prefix_str = get_prefix_ttl_file_str(prefixes)

    if sheet_instance_file_path.suffix == ".csv":
        sheet_instance_file = open(sheet_instance_file_path, "r")
    elif sheet_instance_file_path.suffix == ".xlsx":
        df = pd.read_excel(sheet_instance_file_path)
        sheet_instance_file = io.StringIO(df.to_csv(index=False))
    else:
        raise ValueError(
            "The input file is not one of the supported types: xlsx or csv"
        )

    # read the input graph to get the head node
    input_graph_file_name = re.match(
        r"(.*)-template_sheet.*", sheet_instance_file_path.stem
    ).group(1)
    input_graph_path = next(
        sheet_instance_file_path.parent.glob(f"{input_graph_file_name}.ttl"), None
    )
    if input_graph_path is None:
        raise ValueError(
            "The given folder does not contain the original template input. Did you move or delete it by accident?"
        )
    temp_graph = Graph()
    temp_graph.parse(input_graph_path)
    template_head_prop = URIRef("https://cwrusdle.bitbucket.io/mds/isTemplateHead")
    template_heads = list(temp_graph.subjects(predicate=template_head_prop))
    if len(template_heads) < 1:
        raise ValueError(
            "The template head cannot be found for the file. Did you forget to add `isTemplateHead`?"
        )
    elif len(template_heads) == 1:
        template_head = next(iter(template_heads))
    else:
        options = dict(enumerate(template_heads))
        print("The following heads were identified")
        print("Select from:")
        for idx, option in options.items():
            print(f"{idx}:\t{option}")
        print()
        choice = input("Please select a number corresponding to the correct head:")
        template_head = options[int(choice)]

    _, template_term = split_uri(str(template_head))
    # read file lines
    lines = csv.reader(sheet_instance_file)
    lines = [line for line in lines]

    # remove the metadata line for template name
    template = lines.pop(0)[1]
    types = dict(zip(lines[0], lines[1], strict=False))
    literals = filter(lambda item: item[1] != IRI_VALUE, types.items())
    literals = set(map(lambda item: item[0], literals))
    df = pd.DataFrame(lines[2:], columns=lines[0])

    # get template from working directory if template not specified
    if template_file_path is None:
        template_file_path = sheet_instance_file_path.with_stem(
            sheet_instance_file_path.stem.replace("-template_sheet", "-template")
        ).with_suffix(".stottr")

    # read the original template file to get proper variable order
    orig_headers = []
    with open(template_file_path, 'r') as template_file:
        contents = template_file.read()
        if match := re.search(r'\[(.*)\] :: ', contents):
            orig_headers = match.group(1).split(',')
            orig_headers = [header.replace("?", "").strip() for header in orig_headers]

    # reorder the headers based on the original
    df = df[orig_headers]

    # prepare for term search if input is a class
    search_keys = get_search_keys(inv_prefixes)

    # prepare stottr declaration lines
    stottr_declarations = []

    # prepare additional triples for instantiation if the input is a class
    instance_graph = Graph()

    # iterating over each row and column value
    for _, row in df.iterrows():
        add_terms = []
        head_term = row.get(template_term, None)
        for col, value in row.items():
            new_term = "blank"
            if value.strip() and col in literals:
                new_term = f'"{value}"'
            elif col in literals:
                new_term = "none"
            elif value == "none":
                new_term = value
            elif value.strip() and (
                clean_term := get_abbrev_term_from_str(value).strip().replace(" ", "")
            ):
                if ":" in value:  # if the input is prefixed, assume class matching
                    matching_class = get_best_match(search_keys, value) or URIRef(
                        f"{prefixes[default_prefix]}{clean_term}"
                    )
                    instance_term = rename_col_value(str(col), template_term, head_term)
                    instance_term = replace_string_prefix(prefixes, instance_term)
                    instance_graph.add(
                        (URIRef(instance_term), RDF.type, matching_class)
                    )
                elif head_term is None:
                    new_term = "none"
                else:
                    new_term = f"{default_prefix}:{clean_term}"

            if new_term == "blank":
                if not head_term:
                    print(head_term)
                    new_term = "none"
                else:
                    new_term = rename_col_value(
                        str(col),
                        template_term,
                        head_term,
                        default_prefix=default_prefix,
                    )
            add_terms.append(new_term)

        stottr_declarations.append(f"{template}({','.join(add_terms)}) .\n")
    sheet_instance_file.close()

    ## save the instance graph for merging later
    instance_output_path = output_file_path.with_stem(
        output_file_path.stem.replace("-expanded", "-extra_instances")
    )
    instance_graph.serialize(instance_output_path)

    ## assign unique IDs to each unique term if it is supposed to be a class
    with NamedTemporaryFile(mode="w+", suffix=".ttl") as temp_instance_file:
        temp_instance_file.write(default_prefix_str)
        temp_instance_file.write("\n")
        temp_instance_file.writelines(stottr_declarations)

        temp_instance_file.flush()

        if write_debug_file:
            debug_file_path = output_file_path.with_stem(
                f"{sheet_instance_file_path.stem.replace('-template_sheet', '-debug')}"
            ).with_suffix(".stottr")
            shutil.copy(temp_instance_file.name, debug_file_path)

        lutra_path = get_lutra_path()
        lutra_cmd = f"""
            {lutra_path} -I stottr -l {template_file_path} \
            -L stottr -o {output_file_path} \
            -O wottr \
            -f {temp_instance_file.name}
        """
        subprocess.run(lutra_cmd, shell=True, check=True)
