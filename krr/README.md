# Kernel Ridge Regression

This directory contains all scripts required to run Kernel Ridge Regression (KRR) tasks in this work, along with example outputs.

## 10-fold Cross Validation

To run 10-fold cross validation (CV), use the `10fold_cv.sh` script, which generates a job file.  
Provide the Python script `cross_validation.py`, dataset, representation type, target property, and kernel:

```bash
bash 10fold_cv.sh cross_validation.py TM-GSspinPlus SPAHM_e splitting L
```

This command generates a job file named  
`CV-KRR-{kernel}-{rep}-{prop}-{dataset}.job`.

If you are running on a SLURM-based system, submit the job using `sbatch`. For local execution, simply run the job file with `bash`.

For more details, see **`10fold_cv.sh`** and **`cross_validation.py`**.

## Train/Test Splits

For the Octa-MK dataset, 80/20 train/validation splits from the reference paper  
([DOI: 10.1088/2632-2153/ad9f22](https://doi.org/10.1088/2632-2153/ad9f22)) were also evaluated.

To run these calculations, use the `train_valid_Octa-MK.sh` script, which generates a job file.  
Provide the Python script `final_error.py`, representation type, target property, and kernel:

```bash
bash train_valid_Octa-MK.sh final_error.py SPAHM_e splitting L
```

This command generates a job file named  
`TrainValid-KRR-{kernel}-{rep}-{prop}-{dataset}.job`.

As above, submit the job using `sbatch` on SLURM, or run it locally with `bash`.

For more details, see **`train_valid_Octa-MK.sh`** and **`final_error.py`**.

Example outputs are provided in the **`example_outputs/`** directory.

## Directory Structure

The [`TM-GSspinPlus`](TM-GSspinPlus/) and [`tmPHOTO`](tmPHOTO/) directories contain:

- **`0-repr/`**: NumPy arrays of molecular representations. An example is ε-SPAHM, stored as `SPAHM_e_{dataset}.npy`.
- **`1-prop/`**: Text files containing target properties.
- **`2-cv10-splits/`**: Text files with 10-fold CV train/test indices (folds 0–9, e.g. `0_train_indices.txt`, `0_test_indices.txt`).
- **`krr-hypers-fold0.txt`**: A text file containing the optimal KRR hyperparameters (`eta` and `sigma`) obtained using Q-stack for a given representation, property, and kernel combination.  
  Only the optimal hyperparameters yielding the lowest mean absolute error when training on the first fold (`0_train_indices.txt`, `0_test_indices.txt`) are included, as the optimal values are generally consistent across folds.

The [`Octa-MK`](Octa-MK/) directory contains two subdirectories:

- **`HOMO_LUMO_gap/`**
- **`splitting/`**

Both have the same internal structure as `TM-GSspinPlus` and `tmPHOTO`, with an additional directory:

- **`3-train-valid-meyer/`**: Contains 80/20 train/validation splits (`0-train_indices.txt`, `0-test_indices.txt`) following the reference paper.
