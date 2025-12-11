# Representations

Generate molecular representations (with timing measurements).

------------------------------------------------------------------------

## 1. Move into the dataset directory

``` bash
cd TM-GSspinPlus
```

------------------------------------------------------------------------

## 2. Generate SLURM job scripts and submit

### For representation arrays of the full dataset

#### 2-1. Using QStack (e.g., SPAHM_e)

``` bash
bash ../dataset_submit.sh generate_rep_spahm_qstack.py SPAHM_e qstack TM-GSspinPlus ~/benchmark_tmc/data/TM-GSspinPlus/0-xyz
```

#### 2-2. Using QML2 (e.g., SLATM)

``` bash
bash ../dataset_submit.sh generate_rep_slatm_fchl_qml2.py SLATM qml2 TM-GSspinPlus ~/benchmark_tmc/data/TM-GSspinPlus/0-xyz
```

#### 2-3. Using featomic (e.g., SOAP)

``` bash
bash ../dataset_submit.sh generate_rep_soap_featomic.py SOAP_global cosmo TM-GSspinPlus ~/benchmark_tmc/data/TM-GSspinPlus/0-xyz
```

### Debug mode

To generate representations for **only 10 molecules**:

``` bash
bash ../dataset_submit.sh generate_rep_spahm_qstack.py SPAHM_e qstack TM-GSspinPlus ~/benchmark_tmc/data/TM-GSspinPlus/0-xyz debug
```

*For details, see `dataset_submit.sh` and each Python script.*

------------------------------------------------------------------------

### For a subset (used for measuring timings)

``` bash
bash ../subset_submit.sh generate_rep_spahm_qstack.py SPAHM_e qstack TM-GSspinPlus ~/benchmark_tmc/data/TM-GSspinPlus/0-xyz subset_refcodes/TM-GSspinPlus_sub_0.txt
```

*For details, see `subset_submit.sh` and prepare a text file containing
the refcodes for the subset. Example outputs are provided in the 
`TM-GSspinPlus/examples_output/` folder.*

---

## Notes for the OctaKulik Dataset

Representation generation for **HOMO, LUMO, and gap** (using both low-spin and high-spin geometries)  
and for **splitting** (using only low-spin optimized geometries) is performed **separately**.

See the directories:

- `OctaKulik/HOMO_LUMO_gap/`
- `OctaKulik/splitting/`

---

------------------------------------------------------------------------

# Kernel Timings

Measure Gaussian (G) or Laplacian (L) kernel computation time:

``` bash
bash kernel_submit.sh time_kernel_qstack.py SPAHM_e TM-GSspinPlus/examples_output/SPAHM_e-TM-GSspinPlus-subset.npy TM-GSspinPlus_subset L
```

*For details,see kernel_submit.sh, time_kernel_qstack.py, and the example files in example_kernel/.*
