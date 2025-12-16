# Data

## TM-GSspinPlus
The [`TM-GSspinPlus`](TM-GSspinPlus/) directory contains:
- `0-xyz/`: DFT-optimized geometries with only hydrogen atoms optimized in the lowest-spin state (singlet or doublet)
- `1-extended_xyz/`: Extended XYZ files for MACE with 10 train/test splits for 10-fold cross-validation (CV)
- `2-cv10-splits/`: 10-fold CV index files (indices correspond to row numbers starting from 0 in `TM-GSspinPlus_property.csv`)
- `TM-GSspinPlus_property.csv`: Dataset properties, including:
  - `refcode`: Cambridge Structural Database (CSD) refcode
  - `total_charge`: Total molecular charge
  - `multiplicity`: Ground-state spin multiplicity
  - `splitting`: Vertical spin-splitting energy (kcal/mol)
  - `HOMO`: HOMO energy (eV)
  - `LUMO`: LUMO energy (eV)
  - `gap`: HOMO-LUMO gap (eV)
  - `dipole_moment_Debye`: Dipole moment magnitude (Debye)

## tmPHOTO
The [`tmPHOTO`](tmPHOTO/) directory contains:
- `0-xyz/`: GFN2-xTB optimized geometries (singlet state)
- `1-extended_xyz/`: Extended XYZ files for MACE with 10 train/test splits for 10-fold CV
- `2-cv10-splits/`: 10-fold CV index files (indices correspond to row numbers starting from 0 in `tmPHOTO_property.csv`)
- `tmPHOTO_property.csv`: Dataset properties, including:
  - `refcode`: CSD refcode
  - `total_charge`: Total molecular charge
  - `multiplicity`: Spin multiplicity used in DFT computations (all singlet, 1)
  - `HOMO`: HOMO energy (Hartree)
  - `LUMO`: LUMO energy (Hartree)
  - `gap`: HOMO-LUMO gap (Hartree)
  - `dipole_moment_Debye`: Dipole moment magnitude (Debye)

## OctaKulik
The [`OctaKulik`](OctaKulik/) directory contains:
- `0-xyz/`: DFT-optimized geometries in low-spin (`*_ls.xyz`) or high-spin (`*_hs.xyz`) states
- `1-extended_xyz/`: Extended XYZ files for MACE
  - `HOMO_LUMO_gap/`: 10 train/test splits for HOMO, LUMO, and HOMO-LUMO gap
  - `splitting/`: 10 train/test splits for spin-splitting energy; low-spin optimized geometries and low-spin multiplicities are used
  - `train_valid/`: Train/validation split from the reference paper  
    ([DOI: 10.1088/2632-2153/ad9f22](https://doi.org/10.1088/2632-2153/ad9f22),
    [repository](https://github.com/hjkgrp/many_body_ml)); files with `LS` correspond to spin-splitting energy targets
- `2-dataset_splits/`: contains two subdirectories
  - `HOMO_LUMO_gap/`: indices corresponding to rows (0-based) in `OctaKulik_property_HOMO_LUMO_gap.csv`
  - `splitting/`: indices corresponding to rows (0-based) in `OctaKulik_property_splitting.csv`  
  Each subdirectory contains the directories `2-cv10-splits/` (10-fold CV indices) and `3-train-valid-meyer/`
  (train/validation indices from the reference paper)

- `OctaKulik_train_valid_merged_clean.csv`:  
  The [training data](https://github.com/hjkgrp/many_body_ml/blob/main/data/training_data.csv) and
  [validation data](https://github.com/hjkgrp/many_body_ml/blob/main/data/validation_data.csv) from the reference paper were merged into a single dataset.  
  Refcodes were assigned in this work for convenience. For example, the complex
  *cr_3_[O-]#[C+]_[O-]#[C+]_[O-]#[C+]_[O-]#[C+]_[O-]#[C+]_[O-]#[C+]* in the original training set
  is assigned the refcode `train_0116`, with geometries `train_0116_ls.xyz` (low-spin optimized)
  and `train_0116_hs.xyz` (high-spin optimized).

- `OctaKulik_property_HOMO_LUMO_gap.csv`:
  - `refcode`: Refcode assigned in this work
  - `total_charge`: Total molecular charge
  - `multiplicity`: Spin multiplicity used in the computation
  - `HOMO`: HOMO energy (eV)
  - `LUMO`: LUMO energy (eV)
  - `gap`: HOMO-LUMO gap (eV)

- `OctaKulik_property_splitting.csv`:
  - `refcode`: Refcode assigned in this work
  - `total_charge`: Total molecular charge
  - `multiplicity`: Lowest spin multiplicity among low-spin and high-spin states
  - `splitting`: Vertical spin-splitting energy (kcal/mol)
  - `low_spin`: Low-spin multiplicity
  - `high_spin`: High-spin multiplicity

---
**Note:** To prepare extended XYZ files for MACE, all energy values are converted to eV.  
The following conversion factors are used:
- 1 kcal/mol = 0.0434 eV
- 1 Hartree = 27.2114 eV