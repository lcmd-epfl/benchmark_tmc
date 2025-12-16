#!/bin/env python
import sys
import os
import time
import numpy as np
from ase.io import read
import metatensor
from featomic import SoapPowerSpectrum
from metatensor import Labels
import resource
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
    Generate SOAP representations from XYZ structure files.

    Args:
        rep (str): Representation type ("SOAP_global" or "SOAP").
        paths (list of str): Absolute paths to XYZ files.
        only_z (list of str): Element symbols to include; None for all atoms.
        elements (list of int): Nuclear charges of elements present in the dataset.
    Returns:
        numpy.ndarray: Molecular representation matrix (N_molecules, N_features).
    """
    HYPERS = {
        "cutoff": {
            "radius": 5.0,
            "smoothing": {
                "type": "ShiftedCosine",
                "width": 0.5
            }
        },
        "density": {
            "type": "Gaussian",
            "width": 0.3
        },
        "basis": {
            "type": "TensorProduct",
            "max_angular": 4,
            "radial": {
                "type": "Gto",
                "max_radial": 7
            },
            "spline_accuracy": 1e-06
        }
    }

    calculator = SoapPowerSpectrum(**HYPERS)

    all_neighbors_pairs = Labels(
        names=["neighbor_1_type", "neighbor_2_type"],
        values=np.array([[n_1, n_2] for n_1 in kwargs["elements"] for n_2 in kwargs["elements"]])
    )
    
    mols = [read(xyz) for xyz in kwargs["paths"]]
    
    if rep == "SOAP_global":
        descriptor = calculator.compute(mols)
        descriptor = descriptor.keys_to_samples("center_type")
        descriptor = descriptor.keys_to_properties(all_neighbors_pairs)
        global_descriptor = metatensor.sum_over_samples(descriptor, ["atom", "center_type"])
        reps = global_descriptor.block(0).values
        print(f"{rep} representations generated!")

    elif rep == "SOAP":
        selected_samples_metals = []
        for idx, mol in enumerate(mols) :
            metal_index = np.where([x in kwargs["only_z"] for x in mol.get_chemical_symbols()])[0][0]
            selected_samples_metals.append([idx, metal_index])
        selected_samples_metals = np.array(selected_samples_metals)
        selected_samples = Labels(["system", "atom"], selected_samples_metals)   
 
        descriptor = calculator.compute(mols, selected_samples=selected_samples)
        descriptor = descriptor.keys_to_samples("center_type")
        descriptor = descriptor.keys_to_properties(all_neighbors_pairs)
        reps = descriptor.block(0).values
        print(f"{rep} representations generated!")

    else:
        print(f"The selected representation is not available: {rep}")
        exit(1)

    return reps


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Generates SOAP representations using featomic")
    parser.add_argument("--rep", required=True, type=str, help="Representation type to generate")
    parser.add_argument("--xyz", required=True, type=str, help="Directory path containing the XYZ files")
    parser.add_argument("--debug", action="store_true", help="Enable debugging by truncating the dataset to 10 entries")

    args = parser.parse_args()
    print(vars(args))

    xyzdir = args.xyz

    dataset="OctaKulik"
    df= pd.read_csv("OctaKulik_train_valid_merged_clean.csv")
    all_xyz_paths = []
    for refcode in df["refcode"]:
        all_xyz_paths.append(os.path.join(xyzdir, f"{refcode}_ls.xyz"))
        all_xyz_paths.append(os.path.join(xyzdir, f"{refcode}_hs.xyz"))
    
    only_z = ['Cr', 'Mn', 'Fe', 'Co']
    elements = [1, 6, 7, 8, 9, 15, 16, 17, 24, 25, 26, 27, 53]
 
    if args.debug:
        xyz_paths = all_xyz_paths[:10]
    else:
        xyz_paths = all_xyz_paths

    start = time.perf_counter()
    reps = rep_generator(args.rep, paths=xyz_paths, only_z=only_z, elements=elements)
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


