# Kernel Ridge Regression

## 10-fold Cross Validation

Run 10-fold CV:

``` bash
bash 10fold_cv.sh cross_validation.py TM-GSspinPlus SPAHM_e splitting L
```

For details, see **`10fold_cv.sh`** and **`cross_validation.py`**.


## OctaKulik: Train/Validation Splits from the doi: 10.1088/2632-2153/ad9f22

The original train/validation splits for OctaKulik were also evaluated:

``` bash
bash train_valid_OctaKulik.sh final_error.py SPAHM_e splitting L
```

For details, see **`train_valid_OctaKulik.sh`** and
**`final_error.py`**.


Example outputs are provided in the **`example_outputs/`** folder.
