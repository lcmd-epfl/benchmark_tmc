#!/usr/bin/env python3

import numpy as np
from qstack.regression.kernel_utils import defaults
from qstack.regression.hyperparameters import hyperparameters
from qstack.regression.final_error import final_error
from qstack.tools import correct_num_threads

def main():
    import argparse
    parser = argparse.ArgumentParser(description='10-fold cross-validation (KRR hyperparameters search included).')
    parser.add_argument('--x',      type=str,   dest='repr',       required=True, help='path to the representations file')
    parser.add_argument('--y',      type=str,   dest='prop',       required=True, help='path to the properties file')
    parser.add_argument('--indices',      type=str,   dest='dir_indices',       required=True, help='Path to the directory containing train/test index files for 10-fold CV')
    parser.add_argument('--akernel',     type=str,   dest='akernel',     default=defaults.kernel,    help='local kernel type (G for Gaussian, L for Laplacian, myL for Laplacian for open-shell systems) (default '+defaults.kernel+')')
    parser.add_argument('--print',  type=int,   dest='printlevel', default=0,                  help='printlevel')
    parser.add_argument('--eta',    type=float, dest='eta',   default=defaults.etaarr,   nargs='+', help='eta array')
    parser.add_argument('--sigma',  type=float, dest='sigma', default=defaults.sigmaarr, nargs='+', help='sigma array')
    parser.add_argument('--ll',   action='store_true', dest='ll',       default=False,  help='if correct for the numper of threads')
    parser.add_argument('--save',   action='store_true', dest='save_all',       default=False,  help='if saving intermediate results in .npy file')
    parser.add_argument('--ada',  action='store_true', dest='adaptive', default=False,  help='if adapt sigma')
    parser.add_argument('--readkernel', action='store_true', dest='readk', default=False,  help='if X is kernel')
    parser.add_argument('--name',      type=str,   dest='nameout',       required=True, help='the name of the output file')
    
    args = parser.parse_args()
    
    if(args.readk): args.sigma = [np.nan]
    if(args.ll): correct_num_threads()
    
    print(vars(args))

    X = np.load(args.repr)
    y = np.loadtxt(args.prop)

    dir_indices = args.dir_indices
    
    # List to collect the MAE from each fold
    maes = []
    for i in range(10):
        train_idx = np.loadtxt(f"{dir_indices}/{i}_train_indices.txt", dtype=int)
        test_idx = np.loadtxt(f"{dir_indices}/{i}_test_indices.txt", dtype=int)

        print(f"Number of training samples: {len(train_idx)}, Number of test samples: {len(test_idx)}")

        idx_test=list(test_idx)
        idx_train=list(train_idx)
        
        # Perform KRR hyperparameter optimization on each fold
        if i >= 0:
        # If you want to perform optimization only on the first fold and reuse hyperparameters,
        # uncomment the line below:
        #if i == 0:
            errors = hyperparameters(X[train_idx], y[train_idx], read_kernel=args.readk, sigma=args.sigma, eta=args.eta,
                                     akernel=args.akernel, splits=5, printlevel=args.printlevel, adaptive=args.adaptive)
            errors = np.array(errors)
            mae, stdev, eta, sigma = zip(*errors)
        else :
            pass
        print(i, errors[-1])
        aes, pred = final_error(X, y, sigma=sigma[-1], eta=eta[-1], idx_test=idx_test, idx_train=idx_train,
                                akernel=args.akernel, return_pred=True)

        # Uncomment to save predictions and absolute errors
        #np.save(f"{args.nameout}_pred_{i}", pred)        
        #np.save(f"{args.nameout}_absolute_errors_{i}", aes)
        
        maes.append(np.mean(aes))

    with open(f"{args.nameout}.txt", "w") as f:
        for mae in maes:
            f.write(f"{mae}\n")         

if __name__ == '__main__' : main()
