# Benchmarking Physics-Inspired Machine Learning Models for Transition Metal Complexes

This repository provides datasets and models used to benchmark physics-inspired machine learning methods for property prediction of transition metal complexes with diverse charge and spin states.

## Molecular Representations

For installation, we recommend using the conda environments `qstack`, `qml2`, and `featomic` provided in this repository. Alternatively, you can manually install the corresponding GitHub repositories:

- https://github.com/lcmd-epfl/Q-stack  
- https://github.com/qml2code/qml2  
- https://github.com/metatensor/featomic  

Examples of job scripts and required Python files can be found in the `representations/` directory of this repository.

For kernel ridge regression using molecular representations, see the `krr/` directory.

Precomputed `.npy` files of all molecular representations are available on Materials Cloud.

## 3DMol

For installation instructions and example input files for 3DMol, please refer to:  
https://github.com/lcmd-epfl/3DMol/tree/TMC-benchmark-v0
Trained models are available on Materials Cloud.

## MACE

To install MACE for intensive property prediction, run:

```bash
git clone https://github.com/lcmd-epfl/tmc_mace/tree/intensive
pip install -e .
```
Examples of job scripts are provided in the `mace/` directory of this branch.
Trained models are available on Materials Cloud.



