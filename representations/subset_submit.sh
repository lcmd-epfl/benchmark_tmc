#!/bin/bash -l

# dataset: Name of the dataset
dataset="$1"
# rep: Representation type (SPAHM_e, SLATM, SOAP, etc.)
rep="$2"
# xyz_path: Directory containing the XYZ files
# if realpath is not available
# xyz_path="$(cd "$3" && pwd)"
xyz_path="$(realpath "$3")"

# subset: Path to a text file containing refcodes for the subset (only for TM-GSspinPlus or tmPHOTO)
subset="$(realpath "$4")"

# script: Python script to run depending on dataset and representation type
if [[ "$rep" == "SPAHM_e" || "$rep" == "SPAHM_a_global" || "$rep" == "SPAHM_b_global" || "$rep" == "SPAHM_a" || "$rep" == "SPAHM_b" ]]; then
    script="generate_rep_spahm_qstack.py"
elif  [[ "$rep" == "SLATM" || "$rep" == "aSLATM" || "$rep" == "FCHL_global" || "$rep" == "FCHL" ]]; then
    script="generate_rep_slatm_fchl_qml2.py"
elif  [[ "$rep" == "SOAP_global" || "$rep" == "SOAP" ]]; then
    script="generate_rep_soap_featomic.py"
else
    echo "Error: no such representation type '$rep'"
    exit 1
fi

mem="6GB"
conda_env="benchmark_tmc"  # Conda environment to activate

dir_outputs="example_outputs"
mkdir -p $dir_outputs

job="generate_${rep}_${dataset}_sub"
echo "Running script: $script"
echo "Job filename: ${job}.job"

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

cd ${dataset}
python -u "${script}" --rep "${rep}" --xyz "${xyz_path}" --subset "${subset}"
EOF


