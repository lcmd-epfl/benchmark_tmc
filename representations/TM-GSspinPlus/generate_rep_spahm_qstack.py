#!/bin/env python
import sys
import os
import time
import numpy as np
import qstack
import qstack.spahm.rho as rho
import tqdm
import resource
from qstack.spahm.compute_spahm import get_spahm_representation
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
    Generate eigenvalue-SPAHM, SPAHM(a), or SPAHM(b) representations.

    Args:
        rep (str): Representation type.
        paths (list of str): Absolute paths to XYZ structure files.
        spins (list of int): Spin states (number of unpaired electrons; 
            e.g., singlet=0, doublet=1, triplet=2).
        charges (list of int): Molecular charge states.
        only_z (list of str): Element symbols to include; None for all atoms.
        elements (list of str): Elements present in the dataset.
        max_el (int): Maximum number of electrons.

    Returns:
        numpy.ndarray: Molecular representation matrix (N_molecules, N_features).
    """    
    old_stderr = sys.__stderr__
    if rep == "SPAHM_a":
        mols = [qstack.compound.xyz_to_mol(xyz, basis="minao", charge=charge, spin=spin, ecp="ccpvdzpp")
                for xyz, charge, spin in zip(kwargs["paths"], kwargs["charges"], kwargs["spins"])]
        sys.stderr = old_stderr
        mols = tqdm.tqdm(mols)
        reps = rho.bond.get_repr(mols, kwargs["paths"], guess="LB", rep_type="atom", only_z=kwargs["only_z"],
                                 spin=[mol.spin for mol in mols], auxbasis="def2svpjkfit", elements=kwargs["elements"])
        print(f"{rep} representations generated!")
    elif rep == "SPAHM_a_global":
        mols = [qstack.compound.xyz_to_mol(xyz, basis="minao", charge=charge, spin=spin, ecp="ccpvdzpp")
                for xyz, charge, spin in zip(kwargs["paths"], kwargs["charges"], kwargs["spins"])]
        sys.stderr = old_stderr
        mols = tqdm.tqdm(mols)
        reps = []
        for mol, path in zip(mols, kwargs["paths"]):
            rep_one = rho.bond.get_repr([mol], [path], guess="LB", rep_type="atom", spin=[mol.spin], auxbasis="def2svpjkfit", elements=kwargs["elements"])
            global_rep = np.sum(rep_one, axis=0)
            reps.append(global_rep)

        reps = np.stack(reps, axis=0)
        print(f"{rep} representations generated!")
    elif rep == "SPAHM_b":
        mols = [qstack.compound.xyz_to_mol(xyz, basis="minao", charge=charge, spin=spin, ecp="ccpvdzpp")
                for xyz, charge, spin in zip(kwargs["paths"], kwargs["charges"], kwargs["spins"])]
        sys.stderr = old_stderr
        mols = tqdm.tqdm(mols)
        reps = rho.bond.get_repr(mols, kwargs["paths"], guess="LB", rep_type="bond", only_z=kwargs["only_z"],
                                 same_basis=True, spin=[mol.spin for mol in mols], cutoff=100000, elements=kwargs["elements"])

        print(f"{rep} representations generated!")

    elif rep == "SPAHM_b_global":
        mols = [qstack.compound.xyz_to_mol(xyz, basis="minao", charge=charge, spin=spin, ecp="ccpvdzpp")
                for xyz, charge, spin in zip(kwargs["paths"], kwargs["charges"], kwargs["spins"])]
        sys.stderr = old_stderr
        mols = tqdm.tqdm(mols)
        reps = []
        for mol, path in zip(mols, kwargs["paths"]):
            rep_one = rho.bond.get_repr([mol], [path], guess="LB", rep_type="bond", spin=[mol.spin], same_basis=True, cutoff=100000, elements=kwargs["elements"])
            global_rep = np.sum(rep_one, axis=0)
            reps.append(global_rep)

        reps = np.stack(reps, axis=0)
        print(f"{rep} representations generated!")

    elif rep == "SPAHM_e":
        mols = [qstack.compound.xyz_to_mol(xyz, basis="minao", charge=charge, spin=spin, ecp="ccpvdzpp")
                for xyz, charge, spin in zip(kwargs["paths"], kwargs["charges"],kwargs["spins"])]
        sys.stderr = old_stderr
        mols = tqdm.tqdm(mols)
        reps = []
        for i, (mol, spin) in enumerate(zip(mols, kwargs["spins"])):
            e_spahm = get_spahm_representation(mol, guess_in="LB")
            e_spahm = np.hstack(e_spahm) if spin != None else e_spahm[0]
            nelec = e_spahm.shape[0]
            e_spahm = np.pad(e_spahm, ((0, kwargs["max_el"] - nelec)), mode='constant')
            reps.append(e_spahm)

        reps = np.stack(reps, axis=0)
        print(f"{rep} representations generated!")
    else:
        print(f"The selected representation is not available: {rep}")
        exit(1)
    return reps

def main():
    import argparse
    parser = argparse.ArgumentParser(description="Generates SPAHM representations using qstack")
    parser.add_argument("--rep", required=True, type=str, help="Representation type to generate")
    parser.add_argument("--xyz", required=True, type=str, help="Directory path containing the XYZ files")
    parser.add_argument("--debug", action="store_true", help="Enable debugging by truncating the dataset to 10 entries.")
    parser.add_argument("--subset", type=str, help="Path to a text file containing refcodes for the subset")

    args = parser.parse_args()
    print(vars(args))

    xyzdir = args.xyz
    
    dataset="TM-GSspinPlus"
    df= pd.read_csv("TM-GSspinPlus_property.csv")

    all_xyz_paths = []
    spins = []
    charges = []

    for refcode, total_charge, multiplicity  in zip(df["refcode"], df["total_charge"], df["multiplicity"]):
        all_xyz_paths.append(os.path.join(xyzdir, f"{refcode}.xyz"))
        charges.append(total_charge)
        spins.append(multiplicity)
    
    spins = np.array(spins) -1
    charges = np.array(charges)
    
    only_z = ["Cr", "Mn", "Fe", "Co", "Ni"]
    max_el = 736
    elements = ['B', 'Br', 'C', 'Cl', 'Co', 'Cr', 'F', 'Fe', 'H', 'I', 'Mn', 'N', 'Ni', 'O', 'P', 'S', 'Se', 'Si']

    if args.subset:
        subset_refcodes = np.loadtxt(args.subset, dtype=str)
        subset_indices = df.index[df["refcode"].isin(subset_refcodes)]
        xyz_paths = [all_xyz_paths[idx] for idx in subset_indices]
        spins = spins[subset_indices]
        charges = charges[subset_indices]        
    elif args.debug:
        xyz_paths = all_xyz_paths[:10]
        spins = spins[:10]
        charges = charges[:10]
    else:
        xyz_paths = all_xyz_paths
    
    start = time.perf_counter()
    reps = rep_generator(args.rep, paths=xyz_paths, spins=spins, charges=charges, only_z=only_z, max_el=max_el, elements=elements)
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


