# Packaging Java with the wheel

## Script for building

```{bash}
docker run --rm --platform linux/amd64 -v $(pwd):/io \         
quay.io/pypa/manylinux_2_28_x86_64 \
/bin/bash /io/scripts/build_linux.sh
```

## Script for testing on docker

### Running Kubuntu 22.04 on Docker

```{bash}
docker run -it --rm -v $(pwd)/dist:/dist ubuntu:22.04 /bin/bash
```

### Commands to run inside container

```{bash}
apt-get update && apt-get install -y python3-pip
pip install /dist/asfalto_test-0.1.0-py3-none-manylinux_2_28_x86_64.whl
asfalto
```
