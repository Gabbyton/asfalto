import json
import os
import shutil
from pathlib import Path
from importlib import resources

from rdflib import Graph


def copy_to_workspace(current_file_path: str | Path, new_folder_path: str | Path):
    new_folder_path = Path(new_folder_path)
    new_file_path = (
        new_folder_path / f"{current_file_path.stem}-copy{current_file_path.suffix}"
    )
    shutil.copy(current_file_path, new_file_path)


def get_default_path(rel_path: str | Path) -> Path:
    try:
        return resources.files("asfalto.data") / rel_path
    except (ImportError, FileNotFoundError, ModuleNotFoundError):
        return Path(__file__).parent / "data" / rel_path


def get_refs_path():
    return get_default_path("refs")


def get_default_prefixes_path():
    return get_default_path("default_prefixes.json")


def get_refs_graph():
    ref_graph = Graph()
    refs_path = get_refs_path()
    for file in os.scandir(refs_path):
        ref_graph.parse(file.path)
    return ref_graph


def get_default_prefixes():
    with open(get_default_prefixes_path(), "r") as default_prefixes_file:
        return json.load(default_prefixes_file)
