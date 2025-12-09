#!/bin/bash -l

script="$PWD/time_kernel_qstack.py"
rep_type=$1         # SPAHM_e
rep_file_path=$2    # SPAHM_e-tmPHOTO.npy
akernel=$3          # G or L

job="kernel-${akernel}-${rep_type}"
conda_env="qstack"

# Create job file
cat << EOF > "${job}.job"
#!/bin/bash -l
#SBATCH --job-name=${job}
#SBATCH --mem=16GB
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1

conda activate ${conda_env}

python -u "${script}" --rep_file "${rep_file_path}" --akernel "${akernel}"

EOF

# Submit job
sbatch "${job}.job"
