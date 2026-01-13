from io import StringIO
import os
from pathlib import Path
from tempfile import NamedTemporaryFile

import pandas as pd
from black.linegen import partial
from cemento.rdf.drawio_to_rdf import convert_drawio_to_rdf
from rdflib import Graph
from rdflib import URIRef, Literal
from rdflib.namespace import split_uri

from asfalto.template.constants import get_default_terms
from asfalto.template.io import (
    copy_to_workspace,
    get_default_prefixes,
)
from asfalto.template.preprocessing import (
    get_str_or_abbrev_term,
    get_uri_str,
    get_abbrev_term,
    get_prefix_ttl_file_str,
)
from asfalto.template.transforms import (
    get_prefixes,
    get_classes_and_instances,
    segregate_declaration_template_graph,
)


def generate_template(
    input_path: str | Path,
    output_folder: str | Path,
    template_name: str = None,
    default_prefix: str = "mds",
    export_excel: bool = True,
) -> None:
    input_path = Path(input_path)
    output_path = Path(output_folder)

    # copy the file to the workspace
    if input_path.parent != output_path.parent:
        copy_to_workspace(input_path, output_path)

    full_graph = Graph()

    if ".drawio" in input_path.suffixes:
        with NamedTemporaryFile(
            mode="w+", encoding="utf-8", suffix=".ttl"
        ) as template_input_file:

            temp_input_file = Path(str(template_input_file.name))
            convert_drawio_to_rdf(
                input_path,
                temp_input_file,
                check_errors=True,
                log_substitution_path=(Path(os.getcwd()) / "log.lsp"),
            )
            template_input_file.flush()
            full_graph.parse(temp_input_file)
    else:
        full_graph.parse(input_path)

    default_terms = get_default_terms()
    classes, instances = get_classes_and_instances(full_graph, default_terms)

    declarations_graph, template_graph = segregate_declaration_template_graph(
        full_graph, instances
    )

    prefixes_dict = get_prefixes(template_graph)
    default_prefixes = get_default_prefixes()
    prefixes_dict.update(default_prefixes)

    for prefix, ns in prefixes_dict.items():
        declarations_graph.bind(prefix, ns)
    declarations_file_path = output_path / f"{input_path.stem}-declarations.ttl"
    declarations_graph.serialize(destination=declarations_file_path, format="turtle")

    if template_name is None:
        template_head_prop = URIRef("https://cwrusdle.bitbucket.io/mds/isTemplateHead")
        template_head = next(full_graph.objects(predicate=template_head_prop), None)
        if template_head is None:
            raise ValueError(
                "Cannot automatically name the template if the template head is not defined. Did you forget to add `isTemplateHead`?"
            )
        prefix_uri, original = split_uri(str(template_head))
        inv_prefixes = {str(value): key for key, value in prefixes_dict.items()}
        prefix = inv_prefixes.get(prefix_uri, default_prefix)
        template_name = f"{prefix}:{original}"

    ## Construct the template
    template_terms = {
        term
        for subj, pred, obj in template_graph
        for term in (subj, obj)
        if isinstance(term, URIRef)
    }

    # remove literals from the graph
    literal_triples = [
        (subj, pred, obj)
        for subj, pred, obj in template_graph
        if isinstance(obj, Literal)
    ]

    var_value_iris = dict()
    for triple in literal_triples:
        subj, pred, obj = triple
        label = f"{subj}Value"
        new_iri = URIRef(label)
        template_graph.add((subj, pred, new_iri))
        var_value_iris[subj] = new_iri
        template_graph.remove(triple)

    vars_with_value = {
        var_value_iris[subj]: obj.datatype for subj, _, obj in literal_triples
    }

    template_terms &= set(instances)
    template_terms |= set(vars_with_value.keys())
    template_terms -= classes
    ### generate stottr file of triples
    # TODO: add support for blank nodes or a check against them
    output_sheet_path = output_path / f"{input_path.stem}-template_sheet.csv"
    output_template_path = output_path / f"{input_path.stem}-template.stottr"

    # if the template file already exists, copy its content to merge with final template later
    previous_version_data = None
    if output_sheet_path.exists():
        with open(output_sheet_path, "r") as f:
            lines = f.readlines()
            content = "\n".join(lines[1:])
            previous_version_data = pd.read_csv(StringIO(content))

    with open(output_template_path, "w") as template_file:
        inv_prefixes_dict = {value: key for key, value in prefixes_dict.items()}

        imported_prefixes = get_prefix_ttl_file_str(prefixes_dict)
        template_file.write(imported_prefixes)
        template_file.write("\n" * 3)

        get_triple_str = partial(
            get_str_or_abbrev_term,
            prefixes=inv_prefixes_dict,
            template_terms=template_terms,
        )
        get_uri_short_str = partial(get_uri_str, inv_prefixes=inv_prefixes_dict)
        ottr_triples = [
            f"\tottr:Triple({get_triple_str(subj)}, {get_uri_short_str(pred)}, {get_triple_str(obj)}), \n"
            for subj, pred, obj in template_graph
        ]
        template_term_dict = {term: get_abbrev_term(term) for term in template_terms}
        template_term_dict = dict(sorted(template_term_dict.items()))
        template_input_list = [
            f"? ?{value}" for term, value in template_term_dict.items()
        ]
        template_input = f"{template_name}[{', '.join(template_input_list)}] :: {{\n"
        template_file.write(template_input)
        template_file.writelines(ottr_triples)
        template_file.write("} .\n")

        ### generate sheet
        template_name_line = f"template,{template_name}\n"
        template_var_line = f"{','.join(template_term_dict.values())}\n"
        template_var_types = {
            term: (
                "iri"
                if term not in vars_with_value
                else get_uri_short_str(vars_with_value[term])
            )
            for term in template_term_dict.keys()
        }
        template_var_type_line = f"{','.join(template_var_types.values())}\n"

        output_string = template_var_line + template_var_type_line

        # convert the string into a dataframe
        template_df = pd.read_csv(StringIO(output_string))

        if previous_version_data is not None:
            bool_series = previous_version_data.iloc[2:].notnull().any()
            non_empty_cols = bool_series[bool_series].index.tolist()
            previous_version_data = previous_version_data.get(
                non_empty_cols, pd.DataFrame()
            )
            template_df = previous_version_data.combine_first(template_df)

        if export_excel:
            # FIXME: template name row not added for excel
            excel_output_path = output_sheet_path.with_suffix(".xlsx")
            template_df.to_excel(excel_output_path)
        else:
            with open(output_sheet_path, "w") as f:
                f.write(template_name_line)
                template_df.to_csv(f, index=False, header=True)
