#!/bin/env python
import sys
import os
import time
import numpy as np
import resource
from qml2 import Compound, CompoundList
from qml2.jit_interfaces import array_, concatenate_
from qml2.representations import get_asize, get_convolutions
from qml2.representations import get_slatm_mbtypes
import pandas as pd

def unix_time_decorator(func):
# thanks to https://gist.github.com/turicas/5278558
  def wrapper(*args, **kwargs):
    start_time, start_resources = time.time(), resource.getrusage(resource.RUSAGE_SELF)
    ret = func(*args, **kwargs)
    end_resources, end_time = resource.getrusage(resource.RUSAGE_SELF), time.time()
    print(func.__name__, ':  real: %.4f  user: %.4f  sys: %.4f'%
          (end_time - start_time,
           end_resources.ru_utime - start_resources.ru_utime,
           end_resources.ru_stime - start_resources.ru_stime))
    return ret
  return wrapper

def rep_generator(rep, **kwargs):
    """
    Generate SLATM, FCHL, or cMBDF representations from XYZ structure files.

    Args:
        rep (str): Representation type. Options:
            aSLATM, SLATM, FCHL, FCHL_global, cMBDF, cMBDF_global.
        paths (list of str): Absolute paths to XYZ structure files.
        only_z (numpy.ndarray): Nuclear charges of element symbols to include; 
            None for all atoms.
        elements (numpy.ndarray): Nuclear charges of elements present in the dataset.
        mbtypes (list): Minimal many-body types in the dataset, required for SLATM.
        convolutions (tuple): Convolutions evaluated on a discretized grid,
            required for cMBDF.
         asize (dict): Largest count of each unique element found
            in any molecule in the dataset, required for cMBDF.

    Returns:
        numpy.ndarray: Molecular representation matrix (N_molecules, N_features).
    """    

    old_stderr = sys.__stderr__
    sys.stderr = open("/dev/null", "a")
    compounds = CompoundList([Compound(xyz=xyz) for xyz in kwargs["paths"]])
    sys.stderr = old_stderr
    if rep == "SLATM": # global
        compounds.generate_slatm(mbtypes=kwargs["mbtypes"], local=False)
        merged_reps = array_(compounds.all_representations())
        print(f"{rep} representations generated!")

    elif rep == "aSLATM": # local
        compounds.generate_slatm(mbtypes=kwargs["mbtypes"], local=True, only_z=kwargs["only_z"])
        merged_reps = concatenate_(compounds.all_representations())
        print(f"{rep} representations generated!")

    elif rep == "FCHL_global": # global
        compounds.generate_fchl19(elements=kwargs["elements"])
        global_reps = [np.sum(comp.representation, axis=0) for comp in compounds]
        merged_reps = array_(global_reps)
        print(f"{rep} representations generated!")

    elif rep == "FCHL": # local
        compounds.generate_fchl19(elements=kwargs["elements"])
        target_indices = [np.where([x in kwargs["only_z"] for x in comp.nuclear_charges])[0][0] for comp in compounds]
        local_reps = [comp.representation[idx] for comp, idx in zip(compounds, target_indices)]
        merged_reps = array_(local_reps)
        print(f"{rep} representations generated!")
    
    elif rep == "cMBDF_global": # global
        compounds.generate_cmbdf(kwargs["convolutions"], asize=kwargs["asize"], local=False)
        merged_reps = array_(compounds.all_representations())
        print(f"{rep} representations generated!")
    
    elif rep == "cMBDF": # local
        compounds.generate_cmbdf(kwargs["convolutions"], asize=kwargs["asize"], local=True)
        target_indices = [np.where([x in kwargs["only_z"] for x in comp.nuclear_charges])[0][0] for comp in compounds] 
        local_reps = [comp.representation[idx] for comp, idx in zip(compounds, target_indices)]
        merged_reps = array_(local_reps)
        print(f"{rep} representations generated!")

    else:
        print(f"The selected representation is not available: {rep}")
        exit(1)
    return merged_reps

def main():
    import argparse
    parser = argparse.ArgumentParser(description="Generates representations using qml2")
    parser.add_argument("--rep", required=True, type=str, help="Representation type to generate")
    parser.add_argument("--xyz", required=True, type=str, help="Directory path containing the XYZ files")
    parser.add_argument("--debug", action="store_true", help="Enable debugging by truncating the dataset to 10 entries")
    
    args = parser.parse_args()
    print(vars(args))   
    
    xyzdir = args.xyz
    
    dataset="Octa-MK"
    df= pd.read_csv("Octa-MK_train_valid_merged_clean.csv")
    all_xyz_paths = []
    for refcode in df["refcode"]:
        all_xyz_paths.append(os.path.join(xyzdir, f"{refcode}_ls.xyz"))
        # For representations used to predict spin-splitting energies,
        # comment out the following line (high-spin geometry is not used)
        all_xyz_paths.append(os.path.join(xyzdir, f"{refcode}_hs.xyz"))
    
    only_z = np.array([24, 25, 26, 27])
    elements = np.array([1, 6, 7, 8, 9, 15, 16, 17, 24, 25, 26, 27, 53])
    
    all_compounds = CompoundList([Compound(xyz=xyz) for xyz in all_xyz_paths])
    all_nuclear_charges = all_compounds.all_nuclear_charges()

    # Compute for SLATM
    mbtypes = get_slatm_mbtypes(all_nuclear_charges)
    print("mbtypes length:", len(mbtypes))
    #print(type(mbtypes))

    # Compute for cMBDF
    convolutions = get_convolutions()
    asize = get_asize(all_nuclear_charges)
    print("asize:", asize)
    #print(type(convolutions), type(asize))

    if args.debug:
        xyz_paths = all_xyz_paths[:10]
    else:
        xyz_paths = all_xyz_paths

    start = time.perf_counter()
    reps = rep_generator(args.rep, paths=xyz_paths, only_z=only_z, elements=elements, mbtypes=mbtypes, convolutions=convolutions, asize=asize)
    stop = time.perf_counter()
    elapsed = stop - start

    print("Representation shape:", reps.shape)
    print("Generation time:", elapsed)

    # Output filename
    if args.subset:
        filename = f"{args.rep}-{dataset}-subset"
    elif args.debug:
        filename = f"{args.rep}-{dataset}-debug"
    else:
        filename = f"{args.rep}-{dataset}"

    np.save(filename, reps)

    return 0

if __name__ == '__main__':
    rep_generator = unix_time_decorator(rep_generator)
    main()


