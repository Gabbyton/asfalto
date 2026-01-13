import re

from rdflib import URIRef, Node
from rdflib.namespace import split_uri


def get_str_or_abbrev_term(term: Node, prefixes, template_terms):
    if term in template_terms:
        return f"?{get_abbrev_term(term)}"
    return get_uri_str(term, prefixes)


def get_uri_str(term: Node, inv_prefixes: dict[str, str]) -> str:
    if isinstance(term, URIRef):
        prefix, abbrev_name = split_uri(term)
        return f"{inv_prefixes[prefix]}:{abbrev_name}"
    return str(term)


def get_abbrev_term_from_str(term: str) -> str:
    if ":" in term:
        _, abbrev_name = term.split(":")
        return abbrev_name
    return term


def get_abbrev_term(term) -> str:
    if isinstance(term, URIRef):
        _, abbrev_name = split_uri(term)
        return abbrev_name
    return str(term)


def get_prefix_ttl_file_str(prefixes_dict: dict[str, URIRef]):
    imported_prefixes = [
        f"@prefix {prefix}:\t<{uri}> ." for prefix, uri in prefixes_dict.items()
    ]
    return "\n".join(imported_prefixes)


def get_clean_term(
    term: str,
    prefixes: dict[str, str] | None = None,
    default_prefix: str | None = "mds",
) -> URIRef:
    prefix = None

    if ":" in term:
        prefix, term = term.split(":")
    term = re.sub(r"[^a-zA-Z0-9\-_]+", " ", term.strip())
    words = [(word[0].upper() + word[1:]).strip() for word in re.split(r"\s+", term)]
    new_term = "".join(words)

    if prefix is None:
        prefix = default_prefix

    uri_term = URIRef(f"{prefixes[prefix]}{new_term}")
    return uri_term


def convert_str_to_uriref(term: str, prefixes: dict[str, str]):
    prefix, abbrev_term = term.strip().split(":")
    return URIRef(f"{prefixes[prefix]}{abbrev_term}")
