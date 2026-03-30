from pathlib import Path

import requests
import sys

from asfalto.imports.constants import DEPENDENCIES

try:
    from platformdirs import user_cache_dir
except ImportError:
    from asfalto.utils.io import user_cache_dir


def check_dependencies() -> None:
    base_dir = Path(user_cache_dir("asfalto")) / "jre"
    if not all((base_dir / item).exists() for item in DEPENDENCIES):
        deps = download_deps(DEPENDENCIES, base_dir)
        if not all(output_path for output_path in deps.values()):
            print("Unable to download critical dependencies. Please make sure you have a stable internet connection. The application will now quit.")
            sys.exit(1)


def download_deps(dependencies: dict, output_path: Path) -> dict[str, Path | None] | None:
    try:
        return {item: download_file(url, output_path / item) for item, url in dependencies.items()}
    except (requests.exceptions.Timeout, requests.exceptions.RequestException):
        return None


def download_file(download_url: str, output_path: Path) -> Path | None:
    try:
        print(f"attempting to download {output_path.name} from {download_url}...")
        response = requests.get(download_url, timeout=10)
        response.raise_for_status()
        output_path.write_bytes(response.content)
    except (requests.exceptions.Timeout, requests.exceptions.RequestException):
        print(f"Download failed for {output_path.name}....")
        return None
    return output_path
