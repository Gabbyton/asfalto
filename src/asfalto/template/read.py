import csv
from pathlib import Path

from asfalto.template.io import get_default_prefixes
from asfalto.template.preprocessing import get_prefix_ttl_file_str


def convert_sheet(input_file_path: str | Path, output_path: str | Path):
    stottr_declarations = []
    with open(input_file_path, "r") as f:
        lines = csv.reader(f)
        lines = [line for line in lines]
        template = lines.pop(0)[1]
        # TODO: match to appropriate position instead of hardcoding
        _ = lines.pop(0)
        types = lines.pop(0)
        for line in lines:
            terms = [
                (
                    (term if ":" in term else f"mds:{term}")
                    if types[idx] == "iri"
                    else f'"{term}"'
                )
                for idx, term in enumerate(line)
                if term
            ]
            new_entry = f"{template}({', '.join(terms)}) .\n"
            stottr_declarations.append(new_entry)

    with open(output_path, "w") as f:
        prefixes = get_default_prefixes()
        f.write(get_prefix_ttl_file_str(prefixes))
        f.write("\n")
        f.writelines(stottr_declarations)
