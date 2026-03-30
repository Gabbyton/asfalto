import platform
import os
from pathlib import Path

def user_cache_dir(appname: str) -> str:  # type: ignore[misc]
    system = platform.system()
    if system == "Windows":
        base = os.environ.get("LOCALAPPDATA", Path.home() / "AppData" / "Local")
    elif system == "Darwin":
        base = Path.home() / "Library" / "Caches"
    else:
        base = os.environ.get("XDG_CACHE_HOME", Path.home() / ".cache")
    return str(Path(base) / appname)
