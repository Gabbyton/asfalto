from itertools import chain

from more_itertools.more import zip_broadcast
from rdflib import Graph, Node


def replace_term(
    graph: Graph,
    original: Node,
    replace: Node | None = None,
    remove_previous: bool = True,
):
    replace_subj = zip_broadcast("subj", graph.triples((original, None, None)))
    replace_pred = zip_broadcast("pred", graph.triples((None, original, None)))
    replace_obj = zip_broadcast("obj", graph.triples((None, None, original)))

    triples = list(chain(replace_subj, replace_pred, replace_obj))
    to_remove = map(lambda item: item[1], triples)

    if remove_previous:
        for triple in to_remove:
            graph.remove(triple)

    if replace is None:
        return graph

    to_add = []
    for pos, triple in triples:
        subj, pred, obj = triple
        if pos == "subj":
            to_add.append((replace, pred, obj))
        elif pos == "pred":
            to_add.append((subj, replace, obj))
        else:
            to_add.append((subj, pred, replace))

    for triple in to_add:
        graph.add(triple)

    return graph
