import os
import platform
from importlib.resources import files


def get_java_executable() -> str:
    # Check for bundled JRE inside our package
    # Detect OS
    is_windows = platform.system().lower() == "windows"
    executable_name = "java.exe" if is_windows else "java"
    # Construct path: asfalto -> bin -> jre -> bin -> java(.exe)
    bundled_jre = files("asfalto").joinpath(f"bin/jre/bin/{executable_name}")

    if bundled_jre.exists():
        # Ensure it's executable (sometimes lost in ZIP/Wheels)
        os.chmod(str(bundled_jre), 0o755)
        return str(bundled_jre)

    return "java"  # Fallback to system path


def get_jar_path(item_name: str) -> str:
    java_bin = get_java_executable()
    jar_path = files("asfalto.bin").joinpath(f"{item_name}.jar")

    cmd = " ".join([java_bin, "-jar", str(jar_path)])
    return cmd


def get_robot_path() -> str:
    return get_jar_path("robot")


def get_lutra_path() -> str:
    return get_jar_path("lutra")
