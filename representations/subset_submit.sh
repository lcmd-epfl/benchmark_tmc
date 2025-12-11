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
# subset: Path to a text file containing refcodes for the subset
# for TM-GSspinPlus or tmPHOTO
subset="$6"

# job: SLURM job name
job="generate_${rep}_${dataset}_sub"

mem="64GB"
echo "Running script: $script"
echo "Job name: $job"

# Create job file
cat << EOF > "${job}.job"
#!/bin/bash -l
#SBATCH --job-name=${job}
#SBATCH --mem=${mem}
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH -o ${job}.out
#SBATCH -e ${job}.err

conda activate ${conda_env}

python -u "${script}" --rep "${rep}" --xyz "${xyz_path}" --subset "${subset}"
EOF

# Submit job
sbatch "${job}.job"

