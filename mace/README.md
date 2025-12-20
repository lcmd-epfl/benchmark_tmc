# MACE Training Scripts and Data

This directory contains example scripts and input datasets required to train **MACE** models from scratch.  
All hyperparameters are specified directly in the job (`.job`) files. Job scripts and input data are organized by dataset.

## Model Types

- `*invariant.job`  
  Invariant MACE models (`max_L = 0`) using `model="MACE"` for predicting energies  
  (**splitting**, **HOMO**, **LUMO**, or **gap**).

- `*embedding_invariant.job`  
  Invariant MACE models (`max_L = 0`) using `model="MACE"` with charge and spin embeddings  
  (additional hyperparameter: `--embedding_specs`).

  For energy prediction targets, we additionally tested equivariant MACE models with  
  `max_L = 2` in the Supplementary Information.

- `MACE_dipole*.job`  
  Equivariant MACE models (`max_L = 2`) using `model="AtomicDipolesMACE"` for predicting
  the **dipole moment magnitude**.

## Data Splits

- Each dataset contains a `1-extended_xyz/` directory with MACE input files in extended XYZ format.
- To prepare extended XYZ files for MACE, all energy values are converted to **eV**.
- **10-fold cross-validation (CV)** splits are provided (folds 0–9, for example, `0_train.xyz` and `0_test.xyz`).
- For **OctaKulik**, 10-fold CV splits are provided separately for [`HOMO_LUMO_gap`](OctaKulik/1-extended_xyz/HOMO_LUMO_gap/) and [`splitting`](OctaKulik/1-extended_xyz/splitting/).  
  In addition, a **train–validation split** (as defined in the reference paper) is provided, together with the corresponding job files.  
  See the `--train_file` and `--test_file` in the job scripts under [`OctaKulik`](OctaKulik/).

