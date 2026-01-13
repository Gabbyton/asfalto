import operator
from functools import reduce
from pathlib import Path

from rdflib import Graph, RDF, OWL, URIRef, Node
from rdflib.namespace import split_uri

from asfalto.utils.transforms import replace_term


def retrieve_template_graph(template_path: str | Path, input_head: Node):
    template_graph = Graph()
    template_graph.parse(template_path)
    template_terms = template_graph.subjects(
        predicate=RDF.type, object=OWL.NamedIndividual
    )
    template_head_prop = URIRef("https://cwrusdle.bitbucket.io/mds/isTemplateHead")
    template_head = next(template_graph.subjects(predicate=template_head_prop))
    _, original = split_uri(str(template_head))
    replace_nodes = [
        node for node in template_terms if original in split_uri(str(node))[1]
    ]
    _, replace_str = split_uri(str(input_head))
    replace_dict = {
        term: str(term).replace(original, replace_str) for term in replace_nodes
    }
    for term_to_replace in replace_nodes:
        replacement = URIRef(replace_dict[term_to_replace])
        template_graph = replace_term(template_graph, term_to_replace, replacement)

    # replace  the template head with the head node as well
    template_graph = replace_term(template_graph, template_head, input_head)
    return template_graph, replace_dict


def get_uri_abbrev(term: Node | str):
    _, abbrev = split_uri(str(term))
    return abbrev


def prepare_template_dict(template_source_folder: str | Path):
    template_paths = Path(template_source_folder).rglob("*.ttl")
    template_dict = dict()
    template_def_prop = URIRef("https://cwrusdle.bitbucket.io/mds/isTemplateHead")
    for template_path in template_paths:
        temp_graph = Graph()
        temp_graph.parse(template_path)
        template_variable = next(temp_graph.objects(predicate=template_def_prop), None)
        if template_variable is not None:
            template_dict[template_variable] = template_path
    return template_dict


def normalize_graph(
    input_path: str | Path,
    template_source_folder: str,
    output_path: str | Path | None = None,
):
    graph = Graph()
    graph.parse(input_path)
    if output_path is None:
        output_path = input_path
    if "," in template_source_folder:
        template_source_folder = list(
            map(lambda folder: Path(folder.strip()), template_source_folder.split(","))
        )
    if isinstance(template_source_folder, list):
        template_dicts = map(prepare_template_dict, template_source_folder)
        template_dict = reduce(operator.ior, template_dicts, {})
    else:
        template_dict = prepare_template_dict(template_source_folder)
    template_call_prop = URIRef("https://cwrusdle.bitbucket.io/mds/hasTrait")
    template_triples = graph.subject_objects(predicate=template_call_prop)
    replacement_mapping = dict()
    template_def_prop = URIRef("https://cwrusdle.bitbucket.io/mds/isTemplateHead")
    for original, template_node in template_triples:
        template_path = template_dict.get(template_node, None)
        _, template_node_name = split_uri(str(template_node))
        if template_path is None:
            raise ValueError(
                f"The specified template term {template_node} cannot be mapped"
            )
        template_graph, replace_dict = retrieve_template_graph(template_path, original)
        replace_dict = {
            (original, f"{template_node_name}{get_uri_abbrev(key)}"): URIRef(value)
            for key, value in replace_dict.items()
        }
        replacement_mapping.update(replace_dict)
        inner_template_def_triples = template_graph.triples(
            (None, template_def_prop, None)
        )
        for triple in inner_template_def_triples:
            template_graph.remove(triple)
        graph += template_graph

    # process template subproperties (one level only for now)
    sub_prop = URIRef("https://cwrusdle.bitbucket.io/mds/sub")
    sub_triples = list(graph.subject_objects(predicate=sub_prop))
    for head_node, subprop in sub_triples:
        # FIXME: temporarily require unique suffixes for all subproperties
        orig_subprop = get_uri_abbrev(subprop)
        ref_subprop = orig_subprop[:-1]
        replacement = replacement_mapping[(head_node, ref_subprop)]
        graph = replace_term(graph, subprop, replacement, remove_previous=False)

    # delete internally defined terms
    subprops = list(map(lambda item: item[1], sub_triples))
    for subprop in subprops:
        graph = replace_term(graph, subprop)
    remove_triples = graph.triples_choices((None, [template_call_prop, sub_prop], None))
    for triple in remove_triples:
        graph.remove(triple)
    graph.serialize(output_path)


if __name__ == "__main__":
    normalize_graph("test.ttl", "templates", "test_output.ttl")
