# ASFALTO

`ASFALTO` is a python package for creating, generating and reusing ontology templates to accelerate ontology and Knowledge Graph development, especially for systems with multiple structurally similar components. `ASFALTO` can:

- convert turtle files with named individuals into template sheets over those individuals
- expand a template csv into a turtle file with all specified component variations
- generate reusable templates that can be utilized in other turtle files, enabling bottom-up abstraction 
- perform consistency checks on templates prior to reuse

`ASFALTO` stands for the Abstraction Scaffolding Framework and Automated Linker of Templates for Ontologies. `ASFALTO` is a complementary tool to the [CEMENTO](https://cwru-sdle.github.io/CEMENTO) package.

# Installation

To install `ASFALTO`, use pip or a similar package manager to install the latest version of the package.
```bash
python3 -m venv .asfalto
source .asfalto/bin/activate

pip install asfalto
```

**NOTE:** `ASFALTO` comes with critical dependencies that require `java` to run. If you do not wish to install `java` you can use the `asfalto setup_java` command to cache a platform-specific JRE that the package will use for running the dependencies. In case of failure, please make sure to install a `java` distribution on your system as a fallback. We recommend users install the latest open-source distribution of `java`.  

# Usage

## Important Information

The `ASFALTO` package uses the `lutra` and `ROBOT` packages under the hood. The package checks if these two Java-based dependencies are cached into your system. You may need an internet connection for the first time of use to be able to download and cache these two packages.

## Typical Workflow

To be added on the documentation page.

# Licesne 
