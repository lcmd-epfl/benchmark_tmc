# Benchmarking Physics-Inspired Machine Learning Models for Transition Metal Complexes

This repository provides datasets and scripts for benchmarking physics-inspired machine learning models for property prediction of transition metal complexes with diverse charge and spin states.

## Requirements

The python scripts require NumPy and Pandas.

Install with:

```bash
pip install -r requirements.txt
```

## Molecular Representations

For installation, we recommend using the conda environments `qstack.yml`, `qml2.yml`, and `featomic.yml` provided in this repo. Alternatively, you can manually install the corresponding GitHub repositories:

- https://github.com/lcmd-epfl/Q-stack  
- https://github.com/qml2code/qml2  
- https://github.com/metatensor/featomic  

Examples of job scripts and required Python files can be found in the `representations/` directory of this repo.

For kernel ridge regression using molecular representations, see the `krr/` directory.

Precomputed `.npy` files of all molecular representations are available on Materials Cloud.

## 3DMol

For installation instructions and example input files for 3DMol, please refer to:  
https://github.com/lcmd-epfl/3DMol/tree/TMC-benchmark-v0
Trained models and log files are available on Materials Cloud.

## MACE

To install MACE for intensive property prediction, run:

```bash
git clone https://github.com/lcmd-epfl/tmc_mace/tree/intensive
pip install -e .
```
Examples of job scripts are provided in the `mace/` directory of this branch.
Trained models are available on Materials Cloud.



