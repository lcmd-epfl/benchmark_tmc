# Benchmarking Physics-Inspired Machine Learning Models for Transition Metal Complexes

This repository provides datasets and scripts for benchmarking physics-inspired machine learning models for property prediction of transition metal complexes with diverse charge and spin states.

## Setup
**Prerequisites**
- Python 3.12 or later
- `conda` or `pip`

**Dependencies**
The Python scripts require NumPy, Pandas, and ASE.
```bash
pip install -r requirements.txt
```

## Data
The [`data/`](data/) directory contains all datasets, including XYZ files, property CSV files, extended XYZ files (for MACE), and dataset splits.  
It includes three datasets: **TM-GSspinPlus**, **tmPHOTO**, and **OctaKulik**. 
See the included [README.md](data/README.md) for details.

## Molecular Representations

Packages used to generate molecular representations can be built from source by following the official documentation:

- ε-SPAHM, SPAHM(a), SPAHM(b): [Q-stack](https://github.com/lcmd-epfl/Q-stack)  
  ```bash
  git clone https://github.com/lcmd-epfl/Q-stack
  cd Q-stack
  pip install -e .[spahm,regression]
  ```
- SLATM, FCHL: Install the modified qml2 version below, forked from [qml2](https://github.com/qml2code/qml2).  
  It includes minor updates to atomic SLATM generation without affecting the resulting representations.
  ```bash
  git clone https://github.com/lcmd-epfl/tmc_qml2
  cd tmc_qml2
  pip install -e .
  ```
- SOAP: [featomic](https://github.com/metatensor/featomic), [Documentation](https://docs.metatensor.org/featomic/latest/get-started/installation.html)
  ```bash
  pip install featomic
  ```
Bash scripts for generating `sbatch` job files, together with the required Python scripts, are provided as follows:

- Molecular representation generation (with timing measurements): [`representations/`](representations/)  
  See the included [README.md](representations/README.md) for details.

- Kernel ridge regression using Q-stack: [`krr/`](krr/)  
  See the included [README.md](krr/README.md) for details.

Precomputed NumPy arrays of the molecular representations used in this work are available on [Materials Cloud](https://doi.org/10.24435/materialscloud:6w-xv).

## 3DMol

Installation instructions and example input files for 3DMol are available at:
https://github.com/lcmd-epfl/3DMol/tree/TMC-benchmark-v0  
Trained models and log files are available on [Materials Cloud](https://doi.org/10.24435/materialscloud:6w-xv).

## MACE

Install the modified MACE version for intensive property prediction:
```bash
git clone https://github.com/lcmd-epfl/tmc_mace
cd tmc_mace
git checkout intensive
pip install -e .
```
Example job scripts are provided in [`mace/`](mace/) for each dataset subdirectory. See the included [README.md](mace/README.md) for details.  
Trained models, job scripts, and log files are available on [Materials Cloud](https://doi.org/10.24435/materialscloud:6w-xv).



