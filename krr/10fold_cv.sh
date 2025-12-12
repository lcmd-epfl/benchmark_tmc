#!/bin/bash -l

# script: Python script to run
script="$1"
# dataset: Name of the dataset (used for job naming)
dataset="$2" 
# rep: Representation type (SLATM, FCHL, etc.)
rep="$3"
# prop: Target property (splitting, HOMO, etc.)
prop="$4"
# kernel: Kernel type: G (Gaussian) or L (Laplacian)
kernel="$5"

# X_path: Path to molecular representations file (.npy)
if [[ "$dataset" == "OctaKulik" ]]; then
    if [[ "$prop" == "HOMO" || "$prop" == "LUMO" || "$prop" == "gap" ]]; then
        dir_dataset="${dataset}/HOMO_LUMO_gap"
        X_path="${dir_dataset}/0-repr/${rep}-${dataset}.npy"
    elif [[ "$prop" == "splitting" ]]; then
        dir_dataset="${dataset}/splitting"
        X_path="${dir_dataset}/0-repr/${rep}_LS-${dataset}.npy"
    else
        echo "Error: no such property '$prop' in OctaKulik"
        exit 1
    fi
elif [[ "$dataset" == "TM-GSspinPlus" || "$dataset" == "tmPHOTO" ]]; then
    dir_dataset="${dataset}"
    X_path="${dir_dataset}/0-repr/${rep}-${dataset}.npy"
else
    echo "Error: no such dataset '$dataset'"
    exit 1
fi

# Y_path: Path to target properties file (.txt)
Y_path="${dir_dataset}/1-prop/${prop}-${dataset}.txt"
# dir_indices:  Path to the directory containing train/test index files for 10-fold CV
dir_indices="${dir_dataset}/2-cv10-splits"

if [[ "$kernel" == "L" ]]; then
    akernel="myLfast"
else
    akernel="$kernel"
fi

ncpus=16
mem="64GB"
conda_env="qstack"
dir_outputs="example_outputs"
mkdir -p $dir_outputs
job="CV-KRR-${kernel}-${rep}-${prop}-${dataset}"
echo "Running script: $script"
echo "Job name: $job"

# Generate jobfile
cat << EOF | cat > ${job}.job
#!/bin/bash -l
#SBATCH --job-name=${job}
#SBATCH --mem=${mem}
#SBATCH --tasks=1
#SBATCH --cpus-per-task=${ncpus}
#SBATCH -o ${dir_outputs}/${job}.out
#SBATCH -e ${dir_outputs}/${job}.err

conda activate ${conda_env}

python -u ${script} --x ${X_path} --y ${Y_path} --indices ${dir_indices} --akernel ${akernel} --ada --save --name ${dir_outputs}/${job}

exit 0
EOF

# Submit with slurm
sbatch ${job}.job
