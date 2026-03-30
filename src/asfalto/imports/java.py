from __future__ import annotations

import os
import platform
import shutil
import subprocess
import tarfile
import urllib.request
import zipfile
from pathlib import Path

from asfalto.imports.constants import MIN_JAVA_VERSION, ADOPTIUM_API

try:
    from platformdirs import user_cache_dir
except ImportError:
    from asfalto.utils.io import user_cache_dir


def get_jar_path(item_name: str) -> str:
    java_bin = get_java_executable()
    jar_path = Path(user_cache_dir("asfalto")) / "jre" / f"{item_name}.jar"

    cmd = " ".join([str(java_bin), "-jar", str(jar_path)])
    return cmd


def get_robot_path() -> str:
    return get_jar_path("robot")


def get_lutra_path() -> str:
    return get_jar_path("lutra")


def _cache_dir() -> Path:
    return Path(user_cache_dir("asfalto")) / "jre"


def _java_in_cache() -> Path | None:
    """Return the cached java binary if it exists."""
    cache = _cache_dir()
    binary = "java.exe" if platform.system() == "Windows" else "java"
    candidate = cache / "bin" / binary
    return candidate if candidate.exists() else None


def _system_java() -> Path | None:
    """Return a system java binary if it meets MIN_JAVA_VERSION."""
    # Honour JAVA_OVERRIDE for local dev
    override = os.environ.get("JAVA_OVERRIDE")
    if override:
        return Path(override)

    java = shutil.which("java")
    if java is None:
        return None

    try:
        result = subprocess.run(
            [java, "-version"],
            capture_output=True,
            text=True,
        )
        # `java -version` writes to stderr, e.g. `openjdk version "21.0.1" ...`
        output = result.stderr or result.stdout
        # Extract the major version number
        for token in output.split():
            token = token.strip('"')
            if token.startswith("1."):
                # Old-style: "1.8.0_292" → major = 8
                major = int(token.split(".")[1])
            elif token[0].isdigit():
                major = int(token.split(".")[0])
            else:
                continue
            if major >= MIN_JAVA_VERSION:
                return Path(java)
            else:
                return None  # found Java but too old
    except Exception:
        return None


def _adoptium_url() -> str:
    """Build the Adoptium download URL for the current OS and architecture."""
    system = platform.system()
    machine = platform.machine().lower()

    os_map = {"Darwin": "mac", "Windows": "windows", "Linux": "linux"}
    arch_map = {
        "x86_64": "x64",
        "amd64": "x64",
        "aarch64": "aarch64",
        "arm64": "aarch64",
    }

    adoptium_os = os_map.get(system, "linux")
    adoptium_arch = arch_map.get(machine, "x64")

    return ADOPTIUM_API.format(os=adoptium_os, arch=adoptium_arch)


def get_java_executable() -> Path:
    java = _system_java() or _java_in_cache()
    if java is not None:
        return java

    raise EnvironmentError(
        "No compatible Java runtime found (Java 11+ required).\n"
        "Run `asfalto setup_java` to download one automatically, or set "
        "JAVA_OVERRIDE to point at your local java binary."
    )


def download_jre(force: bool = False) -> Path:
    cached = _java_in_cache()
    if cached and not force:
        print(f"JRE already cached at {cached.parent.parent}")
        return cached

    cache_dir = _cache_dir()
    url = _adoptium_url()
    system = platform.system()
    suffix = ".zip" if system == "Windows" else ".tar.gz"
    archive = cache_dir.parent / f"jre{suffix}"

    cache_dir.parent.mkdir(parents=True, exist_ok=True)

    print(f"→ Downloading JRE from Adoptium...")
    print(f"  URL: {url}")

    def _progress(block_count: int, block_size: int, total: int) -> None:
        if total > 0:
            pct = min(block_count * block_size / total * 100, 100)
            print(f"\r  {pct:.0f}%", end="", flush=True)

    req = urllib.request.Request(url, headers={"User-Agent": "asfalto/1.0"})
    with urllib.request.urlopen(req) as response, open(archive, "wb") as f:
        total = int(response.headers.get("Content-Length", 0))
        downloaded = 0
        block_size = 8192
        while chunk := response.read(block_size):
            f.write(chunk)
            downloaded += len(chunk)
            _progress(downloaded // block_size, block_size, total)
    print()  # newline after progress

    # Remove old cached JRE before extracting
    if cache_dir.exists():
        shutil.rmtree(cache_dir)

    print("→ Extracting...")
    if suffix == ".tar.gz":
        with tarfile.open(archive) as tf:
            tf.extractall(cache_dir.parent)
        # Adoptium tarballs extract to a versioned dir, e.g. jdk-21.0.3+9-jre
        extracted = next(
            p for p in cache_dir.parent.iterdir()
            if p.is_dir() and p.name.startswith("jdk-")
        )
        extracted.rename(cache_dir)
    else:
        with zipfile.ZipFile(archive) as zf:
            zf.extractall(cache_dir.parent)
        extracted = next(
            p for p in cache_dir.parent.iterdir()
            if p.is_dir() and p.name.startswith("jdk-")
        )
        extracted.rename(cache_dir)

    archive.unlink()

    # Ensure java binary is executable (check both possible locations)
    binary_name = "java.exe" if system == "Windows" else "java"
    for candidate in [
        cache_dir / "bin" / binary_name,
        cache_dir / "Contents" / "Home" / "bin" / binary_name,
    ]:
        if candidate.exists():
            if system != "Windows":
                candidate.chmod(0o755)
            binary = candidate
            break
    else:
        raise RuntimeError(
            f"Could not find java binary inside extracted JRE at {cache_dir}.\n"
            "The Adoptium archive layout may have changed. "
            "Please open an issue at https://github.com/Gabbyton/asfalto"
        )

    print(f"JRE cached at {cache_dir}")
    return binary
