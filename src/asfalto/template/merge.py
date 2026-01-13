import subprocess
from pathlib import Path
from tempfile import NamedTemporaryFile
from asfalto.imports.java import get_robot_path

import rdflib
from rdflib import URIRef

from asfalto.template.constants import get_default_terms
from asfalto.template.io import get_refs_graph


def merge(working_dir: str | Path, include_refs: bool = False) -> None:
    working_dir = Path(working_dir)
    if not working_dir.is_dir():
        raise ValueError(
            "Please specify a folder that already ha`s the valid input files."
        )

    required_headers = [
        ("declarations", ".ttl"),
        ("expanded", ".ttl"),
        ("extra_instances", ".ttl"),
    ]
    required_files = {
        header: next(
            filter(
                lambda item: item.match(f"*-{header}*{suffix}"), working_dir.iterdir()
            ),
            None,
        )
        for header, suffix in required_headers
    }

    with (
        NamedTemporaryFile(mode="w+", encoding="utf-8", suffix=".ttl") as merged_file,
        NamedTemporaryFile(
            mode="w+", encoding="utf-8", suffix=".txt"
        ) as term_list_file,
        NamedTemporaryFile(
            mode="w+", encoding="utf-8", suffix=".ttl"
        ) as ref_merged_file,
    ):
        robot_path = get_robot_path()
        header, ref_path = next(iter(required_files.items()))
        output_path = ref_path.with_name(
            f"{ref_path.stem.replace(f'-{header}', '-final')}.ttl"
        )
        intermediate_output_path = merged_file.name if include_refs else output_path
        input_lines = [
            f"--input {input_path} \\"
            for input_path in required_files.values()
            if input_path
        ]
        input_lines = "\n".join(input_lines)
        merge_cmd = f"""
            {robot_path} merge \
            {input_lines}
            --output {intermediate_output_path}
        """
        print(merge_cmd)
        subprocess.run(merge_cmd, shell=True, check=True)

        if include_refs:
            merged_file.flush()

            temp_graph = rdflib.Graph()
            temp_graph.parse(merged_file.name, format="turtle")
            default_terms = get_default_terms()
            terms = {
                term
                for triple in temp_graph
                for term in triple
                if isinstance(term, URIRef) and term not in default_terms
            }
            term_list_file.write("\n".join(terms))
            term_list_file.flush()

            temp_graph += get_refs_graph()
            temp_graph.serialize(destination=ref_merged_file.name, format="turtle")
            ref_merged_file.flush()

            extract_cmd = f"""
                {robot_path} extract \
                --method BOT \
                --input {ref_merged_file.name} \
                --term-file {term_list_file.name} \
                --output {output_path} 
            """
            subprocess.run(extract_cmd, shell=True, check=True)

        print(f"generated final output file in -> {output_path.absolute()}")
