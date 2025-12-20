#!/bin/bash -l

# script: Python script to run
script="$1"
# dataset: Name of the dataset (used for job naming)
dataset="$2"
# rep: Representation type (SLATM, FCHL, etc.)
rep="$3"
# rep_file_path: Path to molecular representations file (.npy)
rep_file_path="$(realpath "$4")"
# kernel: Local kernel type: G (Gaussian) or L (Laplacian)
kernel="$5"


mem="6GB"
conda_env="benchmark_tmc"  # Conda environment to activate

dir_outputs="example_outputs"
mkdir -p $dir_outputs

job="kernel_${kernel}_${rep}_${dataset}"
echo "Running script: $script"
echo "Job name: $job"

# Create job file
cat << EOF > "${job}.job"
#!/bin/bash -l
#SBATCH --job-name=${job}
#SBATCH --mem=${mem}
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH -o ${dir_outputs}/${job}.out
#SBATCH -e ${dir_outputs}/${job}.err
#SBATCH --partition=standard
#SBATCH --time=1-00:00:00

conda activate ${conda_env}

python -u "${script}" --rep_file "${rep_file_path}" --akernel "${kernel}"

EOF
