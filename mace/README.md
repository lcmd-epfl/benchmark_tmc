## MACE Training Scripts and Data

This directory contains SLURM job scripts and input datasets for training **MACE** models from scratch.  
All hyperparameters are specified directly in the job (`.job`) files. Job scripts and input data are organized by dataset.

### Model Types
- `*invariant.job`: invariant MACE (`max_L = 0`) with `model="MACE"`
- `*embedding_invariant.job`: invariant MACE (`max_L = 0`) with `model="MACE"`, including charge and spin embeddings
- Dipole moment magnitude models: equivariant MACE (`max_L = 2`) with `model="AtomicDipolesMACE"`

### Data Splits
- Each dataset contains `1-extended_xyz/` with MACE input files in extended XYZ format
- **10-fold cross-validation** splits are provided (0–9, e.g. `0_train.xyz`, `0_test.xyz`)
- For **OctaKulik**, an additional **train–validation** split (as defined in the original paper) and corresponding job files are available

