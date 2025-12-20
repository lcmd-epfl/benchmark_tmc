# Generate Molecular Representations

This directory contains all scripts required to generate molecular representations, including wall-time measurements.

## Representations for a Full Dataset

To generate molecular representations for an entire dataset, use the `dataset_submit.sh` script.  
Arguments must be provided in the following order: **Dataset name**, **Representation type**, and **Directory path containing XYZ files**.  
For the representation types used in the main text, see [`here`](rep_type.txt).

```bash
bash dataset_submit.sh TM-GSspinPlus SPAHM_e ../data/TM-GSspinPlus/0-xyz
```
This command creates a job file named:
`generate_{rep}_{dataset}.job`

### Debug Mode (10 Molecules)

To generate representations for only 10 molecules (useful for testing and debugging), add the `debug` argument:

```bash
bash dataset_submit.sh TM-GSspinPlus SPAHM_e ../data/TM-GSspinPlus/0-xyz debug
```

This creates a job file named `generate_{rep}_{dataset}_debug.job`

If you are running on a SLURM-based system, submit the job using `sbatch`. For local execution, simply run the job file with `bash`.

## Representations for a Subset

To generate representations for a predefined subset of molecules, use `subset_submit.sh`.  
In addition to the dataset, representation type, and XYZ directory, provide a text file containing refcodes for the subset.

```bash
bash subset_submit.sh TM-GSspinPlus SPAHM_e ../data/TM-GSspinPlus/0-xyz \
TM-GSspinPlus/subset_refcodes/TM-GSspinPlus_sub_0.txt
```

## Related Files and Scripts

For further details, see: 
- `dataset_submit.sh`
- `subset_submit.sh`
- Python scripts in each dataset directory:
  - `generate_rep_spahm_qstack.py`
  - `generate_rep_slatm_fchl_qml2.py`
  - `generate_rep_soap_featomic.py`
- Example output files in `examples_output/*.out`  

Execution timings are reported in the **last line** of each output file.  
The job generates representation arrays (`.npy` files) in the corresponding dataset directory (for example, see [`TM-GSspinPlus`](TM-GSspinPlus/)).


### Notes for the OctaKulik

For representations used to predict **spin-splitting energies**, comment out the lines that include high-spin geometries (or high-spin states).  
See the Python scripts in [`OctaKulik`](OctaKulik/) for details.

# Kernel computations

To measure kernel computation times for Gaussian (G) or Laplacian (L) kernels, use `kernel_submit.sh`.  
Provide the Python script `time_kernel_qstack.py`, dataset name, representation type, path to the `.npy` representation file, and kernel type.

```bash
bash kernel_submit.sh time_kernel_qstack.py TM-GSspinPlus SPAHM_e \
TM-GSspinPlus/SPAHM_e-TM-GSspinPlus-subset.npy L
```

This command generates a job file named:
`kernel_{kernel}_{rep}_{dataset}.job`

For details, see:
- `kernel_submit.sh`
- `time_kernel_qstack.py`
- Example timing outputs in `examples_output/*.out`.  

Execution timings are reported in the **last line** of the corresponding output file.