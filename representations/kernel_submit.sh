#!/bin/bash -l

# script: Python script to run
script="$1"
# rep: Representation type (SLATM, FCHL, etc.)
rep="$2"
# rep_file_path: Path to molecular representations file (.npy)
rep_file_path="$3"
# dataset: Name of the dataset (used for job naming)
dataset="$4"
# akernel: Local kernel type: G (Gaussian) or L (Laplacian)
akernel="$5"

conda_env="qstack"
job="kernel_${akernel}_${rep}_${dataset}"
echo "Running script: $script"
echo "Job name: $job"

# Create job file
cat << EOF > "${job}.job"
#!/bin/bash -l
#SBATCH --job-name=${job}
#SBATCH --mem=16GB
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH -o ${job}.out
#SBATCH -e ${job}.err

conda activate ${conda_env}

python -u "${script}" --rep_file "${rep_file_path}" --akernel "${akernel}"

EOF

# Submit job
sbatch "${job}.job" || bash "${job}.job"
