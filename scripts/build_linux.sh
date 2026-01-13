#!/bin/bash
set -e

# 1. Install the full suite of modules
# Adding '*' ensures we get java-17-openjdk-java.sql, etc.
dnf install -y java-17-openjdk-devel java-17-openjdk-jmods

# 2. Dynamically locate JAVA_HOME and JMODS
# In many-linux containers, this is usually /usr/lib/jvm/java-17-openjdk
JAVA_HOME=$(dirname $(dirname $(readlink -f $(which javac))))
JMODS_PATH="$JAVA_HOME/jmods"

echo "Using JAVA_HOME: $JAVA_HOME"
echo "Looking for JMODS in: $JMODS_PATH"
echo "Checking JMODS directory contents:"
ls "$JMODS_PATH"

# 3. Create a minimal JRE
# We explicitly add the --module-path pointing to the JMODS folder
# 1. Find which modules the JAR actually uses
echo "Analyzing JAR dependencies..."
MODULES=$(jdeps --ignore-missing-deps --print-module-deps /io/src/asfalto/bin/robot.jar 2>/dev/null | grep -v "Warning" | tr -d '\n\r ')

# 2. Safety check: ensure java.base is included and the string isn't empty
if [ -z "$MODULES" ]; then
    MODULES="java.base"
else
    # Remove any potential trailing commas and add java.base if not present
    MODULES="${MODULES},java.base"
fi

echo "Cleaned Modules list: $MODULES"

# 3. Create the JRE
# Clear previous output directory if it exists
rm -rf /io/src/asfalto/bin/jre

$JAVA_HOME/bin/jlink \
    --module-path "$JMODS_PATH" \
    --add-modules "$MODULES" \
    --strip-debug \
    --no-man-pages \
    --no-header-files \
    --compress=2 \
    --output /io/src/asfalto/bin/jre

echo "Testing bundled JRE..."
/io/src/asfalto/bin/jre/bin/java --version

# 4. Build the Wheel
# Use 'pip wheel' as it is more robust in these containers
/opt/python/cp310-cp310/bin/pip wheel /io/ --no-deps -w /io/dist/

# 5. Manually Tag the Wheel
# We rename "any" to "manylinux_2_28_x86_64" so pip knows this is the Linux version
cd /io/dist/
for f in *-any.whl; do
    mv "$f" "${f//-any/-manylinux_2_28_x86_64}"
done

echo "Build complete. Wheel located in dist/"