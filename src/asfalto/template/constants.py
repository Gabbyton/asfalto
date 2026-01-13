from rdflib import SKOS, RDF, RDFS, OWL, DCTERMS

IRI_VALUE = "iri"


def get_default_terms():
    default_namespaces = [SKOS, RDF, RDFS, OWL, DCTERMS]
    return {term for ns in default_namespaces for term in dir(ns)}
