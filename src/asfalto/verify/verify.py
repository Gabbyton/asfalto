import subprocess
from pathlib import Path
from tempfile import NamedTemporaryFile

from cemento.rdf.drawio_to_rdf import convert_drawio_to_rdf
from rdflib import Graph, URIRef

from asfalto.imports.java import get_robot_path
from asfalto.template.io import get_refs_graph


def verify_template(
    onto_input_path: str | Path,
    reason_output_path: str | Path | None = None,
    substitution_debug_path: str | Path | None = None,
) -> None:
    onto_input_path = Path(onto_input_path)
    if reason_output_path is None:
        reason_output_path = onto_input_path.with_stem(
            f"{onto_input_path.stem}-reason"
        ).with_suffix(".md")
    reason_output_path = str(reason_output_path)

    print(
        f"performing reasoning on input {onto_input_path}. The results will be saved in {reason_output_path}..."
    )

    full_graph = Graph()

    if onto_input_path.suffix == ".drawio":
        with NamedTemporaryFile(
            mode="w+", encoding="utf-8", suffix=".ttl"
        ) as temp_rdf_file:
            temp_rdf_file_path = Path(str(temp_rdf_file.name))
            convert_drawio_to_rdf(
                onto_input_path,
                temp_rdf_file_path,
                check_errors=True,
                log_substitution_path=substitution_debug_path,
            )
            temp_rdf_file.flush()
            full_graph.parse(temp_rdf_file_path)
    else:
        full_graph.parse(onto_input_path)

    ref_graph = get_refs_graph()

    with (
        NamedTemporaryFile(mode="wb+", suffix=".ttl") as all_graph_file,
        NamedTemporaryFile(mode="wb+", suffix=".ttl") as ref_graph_file,
        NamedTemporaryFile(mode="w+", suffix=".txt") as term_list_file,
    ):
        all_graph_contents = full_graph.serialize(format="turtle", encoding="utf-8")
        ref_graph_contents = ref_graph.serialize(format="turtle", encoding="utf-8")
        all_graph_file.write(all_graph_contents)
        ref_graph_file.write(ref_graph_contents)
        term_list_file.writelines(
            "\n".join(
                [
                    term
                    for triple in full_graph
                    for term in triple
                    if isinstance(term, URIRef)
                ]
            )
        )
        all_graph_file.flush()
        ref_graph_file.flush()
        term_list_file.flush()

        reason_cmd = f"""
            {get_robot_path()} extract --method BOT \
            --input {ref_graph_file.name} \
            --term-file {term_list_file.name} \
            merge --input {all_graph_file.name} \
            explain --reasoner hermit \
            -M inconsistency \
            --explanation {reason_output_path} \
            --max 25
        """

        subprocess.run(reason_cmd, shell=True)
