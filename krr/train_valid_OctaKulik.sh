#!/bin/bash -l

# script: Python script to run $PWD/final_error.py
script="$1"
# dataset: Name of the dataset (used for job naming)
dataset="OctaKulik"
# rep: Representation type (SLATM, FCHL, etc.)
rep="$2"
# prop: Target property (splitting, HOMO, etc.)
prop="$3"
# kernel: Kernel type: G (Gaussian) or L (Laplacian)
kernel="$4"

# X_path: Path to molecular representations file (.npy)
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

# Y_path: Path to target properties file (.txt)
Y_path="${dir_dataset}/1-prop/${prop}-${dataset}.txt"
# train_idx: a txt file containing the training set indices 
train_idx="${dir_dataset}/3-train-valid-meyer/0-train_indices.txt"
# test_idx: a txt file containing the test set indices
test_idx="${dir_dataset}/3-train-valid-meyer/0-test_indices.txt"

if [[ "$kernel" == "L" ]]; then
    akernel="myLfast"
else
    akernel="$kernel"
fi

ncpus=16
mem="32GB"
conda_env="benchmark_tmc"

dir_outputs="example_outputs"
mkdir -p $dir_outputs

job="TrainValid-KRR-${kernel}-${rep}-${prop}-${dataset}"
echo "Running script: $script"
echo "Job filename: ${job}.job"

# Generate jobfile
cat << EOF | cat > ${job}.job
#!/bin/bash -l
#SBATCH --job-name=${job}
#SBATCH --mem=${mem}
#SBATCH --tasks=1
#SBATCH --cpus-per-task=${ncpus}
#SBATCH -o ${dir_outputs}/${job}.out
#SBATCH -e ${dir_outputs}/${job}.err
#SBATCH --partition=standard
#SBATCH --time=1-00:00:00

conda activate ${conda_env}

python -u ${script} --x ${X_path} --y ${Y_path} --train_idx ${train_idx} --test_idx ${test_idx} --akernel ${akernel} --ada --save --name ${dir_outputs}/${job}

exit 0
EOF
