#!/bin/bash -l

# script: Python script to run
script="$1"
# rep: Representation type (SLATM, FCHL, etc.)
rep="$2"
# conda_env: Conda environment to activate
conda_env="$3"
# dataset: Name of the dataset (used for job naming)
dataset="$4"
# xyz_path: Directory containing the XYZ files
xyz_path="$5"
# debug_flag: Add "--debug" if the 6th argument is "debug"
# Enable debugging by truncating the dataset to 10 entries
debug_flag=""
if [ "$6" == "debug" ]; then
    debug_flag="--debug"
    job="generate_${rep}_${dataset}_debug"
else
    job="generate_${rep}_${dataset}"
fi

ncpus=16
mem="128GB"
echo "Running script: $script"
echo "Job name : $job"

# Create job file
cat << EOF > "${job}.job"
#!/bin/bash -l
#SBATCH --job-name=${job}
#SBATCH --mem=${mem}
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=$ncpus
#SBATCH -o ${job}.out
#SBATCH -e ${job}.err

conda activate ${conda_env}

python -u "${script}" --rep "${rep}" --xyz "${xyz_path}" ${debug_flag}
EOF

# Submit job
sbatch "${job}.job"

