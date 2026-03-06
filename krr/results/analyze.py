import sys
import os
import numpy as np


raw_data = np.loadtxt("./LC_SPAHM_e-TM-GSspinPlus.npy_splitting-TM-GSspinPlus.txt_predictions.txt", dtype=float)
nsamples, nsplits = raw_data.shape[0], raw_data.shape[1]/2

split_pairs = np.array([(raw_data[:,i], raw_data[:,i+1]) for i in np.arange(0, 20, 2)])
print(split_pairs.shape)

with open("HS_LS_splits-mae.dat", "w") as fout:
    print("# split HS-mae LS-mae", file=fout)
    for i,s in enumerate(split_pairs):
        targs, preds = s
        ls_mae = np.mean([np.abs(t-p) for t,p in zip(targs, preds) if t > 0])
        hs_mae = np.mean([np.abs(t-p) for t,p in zip(targs, preds) if t < 0])
        print(f"Split = {i} : LS-mae = {ls_mae} and HS-mae = {hs_mae}")
        print(f"{i} {hs_mae} {ls_mae}", file=fout)
