from copy import deepcopy
from itertools import chain

import thefuzz.process
from more_itertools.more import map_reduce
from more_itertools.recipes import unique_everseen
from rdflib import Graph, URIRef, RDF, RDFS, Node, BNode
from rdflib import SKOS
from rdflib.namespace import split_uri
from thefuzz import fuzz

from asfalto.template.constants import get_default_terms
from asfalto.template.io import get_refs_graph
from asfalto.template.preprocessing import (
    get_uri_str,
)


def get_prefixes(graph: Graph):
    return {prefix: uri for prefix, uri in graph.namespaces()}


def get_prefix(term: URIRef, inv_prefixes: dict[str, str]) -> str | None:
    prefix, _ = split_uri(term)
    return inv_prefixes.get(prefix, None)


def get_search_keys(inv_prefixes: dict[str, str]):
    ref_graph = get_refs_graph()
    ref_graph_terms = chain(
        ref_graph.subjects(predicate=RDFS.subClassOf),
        ref_graph.subjects(predicate=RDF.type),
    )
    default_terms = get_default_terms()
    all_terms = unique_everseen(chain(ref_graph_terms, default_terms))
    all_terms = filter(lambda item: isinstance(item, URIRef), all_terms)
    all_terms = list(all_terms)
    alt_label_triples = ref_graph.triples_choices((all_terms, SKOS.altLabel, None))
    label_triples = ref_graph.triples_choices((all_terms, RDFS.label, None))
    aliases = map_reduce(
        chain(alt_label_triples, label_triples),
        keyfunc=lambda t: t[0],
        valuefunc=lambda t: str(t[2]),
    )
    alias_mapping = {
        f"{get_prefix(key, inv_prefixes)}:{value}": key
        for (key, values) in aliases.items()
        for value in values
    }
    abbrev_term_mapping = {
        get_uri_str(term, inv_prefixes): term
        for term in chain(ref_graph_terms, default_terms)
    }
    alias_mapping.update(abbrev_term_mapping)
    return alias_mapping


def get_best_match(candidates: dict[str, URIRef], term: str) -> Node | None:
    result = thefuzz.process.extractOne(
        term,
        candidates.keys(),
        scorer=fuzz.partial_ratio,
        score_cutoff=90,
    )

    if result is None:
        return None

    result, _ = result
    result = candidates[result]

    return result


def get_classes_and_instances(graph: Graph, default_terms: set[URIRef]):
    classes = set()
    instances = set()

    for subj, pred, obj in graph:
        if isinstance(subj, URIRef) and isinstance(obj, URIRef):
            if pred == RDF.type and obj not in default_terms:
                instances.add(subj)
                classes.add(obj)

            if pred == RDFS.subClassOf:
                classes.update({subj, obj})

    instances = list(instances)
    return classes, instances


def bind_prefixes(graph: Graph, *source_graphs: Graph) -> Graph:
    prefixes = {
        (prefix, ns)
        for source_graph in source_graphs
        for (prefix, ns) in source_graph.namespaces()
    }
    for prefix, ns in prefixes:
        graph.bind(prefix, str(ns))
    return graph


def segregate_declaration_template_graph(
    graph: Graph, instances: set[URIRef]
) -> tuple[Graph, Graph]:
    # TODO: check that axioms are only declared for classes in declarations
    declarations_graph = deepcopy(graph)
    # NOTE: do not allow for blank nodes in template declarations! Do so in template parsing, which will be added once useful
    instances = list(instances)
    template_triples = unique_everseen(
        chain(
            graph.triples_choices((instances, None, None)),
            graph.triples_choices((None, None, instances)),
        )
    )
    template_triples = filter(
        lambda triple: not isinstance(triple[0], BNode)
        and not isinstance(triple[2], BNode),
        template_triples,
    )

    template_graph = Graph()
    for triple in template_triples:
        template_graph.add(triple)

    ## save declarations graph to output folder for later merging
    declarations_graph = declarations_graph - template_graph

    return declarations_graph, template_graph
