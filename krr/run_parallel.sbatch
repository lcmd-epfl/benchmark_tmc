#! /usr/bin/env bash
#
#SBATCH --ntasks 1
#SBATCH --nodes 1
#SBATCH --cpus-per-task=256
#SBATCH --time 02:00:00
#SBATCH --exclusive
#SBATCH --mem 450GB
#SBATCH --array=0-2
#SBATCH -A mr31
#SBATCH -C mc

usage(){
	echo "usage: $0 [-dhD] -x REPFILE -y PROPFILE
	-x) .npy file containing array of representations
	-y) .txt file containing the target properties
	-d) enables debug run
	-h) shows help"
}

debug=0
while getopts "dhDx:y:" opt;do
	case $opt in
	d)	debug=1;;
	x)	xfile=$OPTARG;;
	y)	yfile=$OPTARG;;
	h)
		usage
		exit 1;;
	?)
		usage
		exit 1;;
	esac
done

if [[ $# < 1 ]];then
	usage
	exit 1
fi
	
NPROC=64

export OMP_NUM_THREADS=1
export OPENBLAS_NUM_THREADS=1
export MKL_NUM_THREADS=1

total_cpus=$((OMP_NUM_THREADS*NPROC))
opts=()
if [[ $debug == 1 ]];then
	opts+=("--debug")
fi
if [[ $diffmode == 1 ]];then
	opts+=("--diff")
fi


python run_CV-parallel.py --prop $yfile  --rep $xfile --nproc $NPROC --out results/ ${opts[@]}
