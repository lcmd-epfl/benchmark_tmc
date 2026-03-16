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
It includes three datasets: **TM-GSspinPlus**, **tmPHOTO**, and **Octa-MK**. 
See the included [README.md](data/README.md) for details.

## Molecular Representations

Packages used to generate molecular representations can be built from source by following the official documentation:

- ε-SPAHM, SPAHM(a), SPAHM(b): [Q-stack](https://github.com/lcmd-epfl/Q-stack)  
  ```bash
  git clone https://github.com/lcmd-epfl/Q-stack
  cd Q-stack
  git checkout TMC-benchmark-v1
  pip install -e .[spahm,regression]
  ```
- SLATM, FCHL: Install the modified qml2 version below, forked from [qml2](https://github.com/qml2code/qml2).  
  It includes minor updates to atomic SLATM generation without affecting the resulting representations.
  ```bash
  git clone https://github.com/lcmd-epfl/tmc_qml2
  cd tmc_qml2
  git checkout TMC-benchmark-v1
  pip install -e .
  ```
- SOAP: [featomic](https://github.com/metatensor/featomic), [Documentation](https://docs.metatensor.org/featomic/latest/get-started/installation.html)
  ```bash
  pip install featomic
  ```
Bash scripts for generating job files, along with the required Python scripts, are provided under:

- Molecular representation generation and kernel computations (including timing measurements): [`representations/`](representations/)  
  See the included [README.md](representations/README.md) for details.

- Kernel ridge regression using Q-stack: [`krr/`](krr/)  
  See the included [README.md](krr/README.md) for details.

Precomputed NumPy arrays of the molecular representations used in this work are available on [Materials Cloud](https://doi.org/10.24435/materialscloud:pv-nj).

## Geometric deep learning models
### 3DMol

Installation instructions and example input files are available in [3DMol](https://github.com/lcmd-epfl/3DMol/tree/TMC-benchmark-v1) (tag `TMC-benchmark-v1`).
Trained models and log files are available on [Materials Cloud](https://doi.org/10.24435/materialscloud:pv-nj).

### MACE

Install the modified MACE version for intensive property prediction:
```bash
git clone https://github.com/lcmd-epfl/tmc_mace
cd tmc_mace
git checkout TMC-benchmark-v1
pip install -e .
```
Example job scripts and train/test extended XYZ files are provided in [`mace/`](mace/) for each dataset subdirectory.  
See the included [README.md](mace/README.md) for details. Trained models, job scripts, and log files are available on [Materials Cloud](https://doi.org/10.24435/materialscloud:pv-nj).

### NatQG
Natural quantum graph (NatQG)-based GNN models are additionally evaluated for predicting the HOMO-LUMO gap and dipole moment magnitude on a **subset of tmPHOTO**. 
Further details are available in [tmc_NatQG](https://github.com/lcmd-epfl/tmc_NatQG/tree/TMC-benchmark-v1) (tag `TMC-benchmark-v1`).

## Environments

Two Conda environment files are provided as references.  
Both environments were built on **Red Hat Enterprise Linux 9.4 (Plow), x86_64**.


### Benchmark Environment

The environment file [`environment_x86_64-rhel_9.yml`](environment_x86_64-rhel_9.yml) includes all dependencies required for molecular representation generation and kernel benchmarking, including the following packages:
- `qstack`
- `qml2`
- `featomic`
- `mace`

```bash
conda env create -f environment_x86_64-rhel_9.yml
conda activate benchmark_tmc
```

### MACE-Only Environment

This mace environment [`mace_x86_64-rhel_9.yml`](mace_x86_64-rhel_9.yml) includes only the dependencies required for training MACE models. It is compatible with RHEL 9.

```bash
conda env create -f mace_x86_64-rhel_9.yml
conda activate mace
```
