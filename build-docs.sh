sphinx-build -M html docs-src/source docs-src/build
mkdir -p docs
cp -r docs-src/build/html/* docs/