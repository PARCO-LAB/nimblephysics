![Stanford Nimble Logo](https://nimblephysics.org/README/README_Splash.svg)

[![Tests](https://github.com/nimblephysics/nimblephysics/actions/workflows/ci_docker.yml/badge.svg)](https://github.com/nimblephysics/nimblephysics/actions/workflows/ci_docker.yml)

# Stanford Nimble

`pip3 install nimblephysics-parco`

### Build a local wheel

If you want to use this checkout in another project, build and install the wheel:

```bash
python -m venv .venv-build
.venv-build/bin/python -m pip install --upgrade pip setuptools wheel build pybind11 pybind11-stubgen
.venv-build/bin/python setup.py bdist_wheel
.venv-build/bin/python -m pip install --force-reinstall dist/nimblephysics_parco-*.whl
```

If you are building from a fresh clone, populate `.deps/` first. The build will
recreate local helper symlinks such as `Eigen` and `unsupported` if your
environment needs them, then you can rerun `setup.py bdist_wheel`.

### Install from a wheel

For a local wheel file:

```bash
python -m pip install /path/to/nimblephysics_parco-*.whl
```

For a wheel published on GitHub Releases:

```bash
python -m pip install https://github.com/<org>/<repo>/releases/download/<tag>/nimblephysics_parco-*.whl
```

On Linux, make sure the runtime library paths used by the wheel are available
on the target machine too.

If you're developing inside this repo, use an editable install:

```bash
python -m pip install -e .
```

** BETA SOFTWARE **

This repository provides a PyTorch-enabled physics engine with analytical
backpropagation through simulation steps.

![Forward pass illustration](https://nimblephysics.org/README/README_DataFlow_Fwd.svg)

It also supports an analytical backwards pass, even through contact and
friction.

![Backpropagation illustration](https://nimblephysics.org/README/README_DataFlow_Back.svg)

It's as easy as:

```python
from nimble import timestep

# Everything is a PyTorch Tensor, and this is differentiable!!
next_state = timestep(world, current_state, control_forces)
```
