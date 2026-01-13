import subprocess
import sys
import platform
from importlib.resources import files
import os

def get_java_executable():
    # Check for bundled JRE inside our package
    # Detect OS
    is_windows = platform.system().lower() == "windows"
    executable_name = "java.exe" if is_windows else "java"
    # Construct path: asfalto -> bin -> jre -> bin -> java(.exe)
    bundled_jre = files('asfalto').joinpath(f'bin/jre/bin/{executable_name}')
    
    if bundled_jre.exists():
        # Ensure it's executable (sometimes lost in ZIP/Wheels)
        os.chmod(str(bundled_jre), 0o755)
        return str(bundled_jre)
    
    return "java"  # Fallback to system path

def run_robot():
    # 1. Locate the JAR file inside the installed package
    # This works even if the package is zipped or installed in a virtualenv
    java_bin = get_java_executable()
    jar_path = files('asfalto.bin').joinpath('robot.jar')
    
    # 2. Build the command
    # We pass along any arguments provided to the shell command (sys.argv[1:])
    cmd = [java_bin, "-jar", str(jar_path)] + sys.argv[1:]
    
    try:
        # 3. Execute
        subprocess.run(cmd, check=True)
    except FileNotFoundError:
        print("Error: Java is not installed or not in PATH.", file=sys.stderr)
        sys.exit(1)
    except subprocess.CalledProcessError as e:
        sys.exit(e.returncode)

if __name__ == "__main__":
    run_robot()