# Benchmarking Physics-Inspired Machine Learning Models for Transition Metal Complexes

This repository provides datasets and scripts for benchmarking physics-inspired machine learning models for property prediction of transition metal complexes with diverse charge and spin states.

## Setup
**Prerequisites**
- Python 3.9 or later
- `conda` or `pip`

**Dependencies**
The Python scripts require NumPy, Pandas, and ASE.
```bash
pip install -r requirements.txt
```

## Molecular Representations
Molecular representation packages can be built from source by following the official documentation:
- ε-SPAHM, SPAHM(a), SPAHM(b): https://github.com/lcmd-epfl/Q-stack  
- SLATM, FCHL: https://github.com/qml2code/qml2  
- SOAP: https://github.com/metatensor/featomic  

Example job scripts and required Python files are provided in the `representations/`.
Kernel ridge regression examples using molecular representations are available in `krr/`.
Numpy array of molecular representations used in this work are available on Materials Cloud.

## 3DMol

Installation instructions and example input files for 3DMol are available at:
https://github.com/lcmd-epfl/3DMol/tree/TMC-benchmark-v0
Trained models and log files are available on Materials Cloud.

## MACE

Install the modified MACE version for intensive property prediction:
```bash
git clone https://github.com/lcmd-epfl/tmc_mace.git
cd tmc_mace
git checkout intensive
pip install -e .
```
Example job scripts are provided in `mace/` for each dataset subdirectory.
Trained models, job scripts, and log files are available on Materials Cloud.



