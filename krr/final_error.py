#!/usr/bin/env python3

import numpy as np
from qstack.regression.kernel_utils import defaults, ParseKwargs
from qstack.regression.hyperparameters import hyperparameters
from qstack.regression.final_error import final_error
from qstack.tools import correct_num_threads

def main():
    import argparse
    parser = argparse.ArgumentParser(description='Train/valid splits for Octakulik (KRR hyperparameters search included).')
    parser.add_argument('--x',      type=str,   dest='repr',       required=True, help='path to the representations file')
    parser.add_argument('--y',      type=str,   dest='prop',       required=True, help='path to the properties file')
    parser.add_argument('--akernel',     type=str,   dest='akernel',     default=defaults.kernel,    help='local kernel type (G for Gaussian, L for Laplacian, myL for Laplacian for open-shell systems) (default '+defaults.kernel+')')
    parser.add_argument('--gkernel',     type=str,   dest='gkernel',     default=defaults.gkernel,    help='global kernel type (avg for average kernel, rem for REMatch kernel) (default )')
    parser.add_argument('--gdict',     nargs='*',   action=ParseKwargs, dest='gdict',     default=defaults.gdict,    help='dictionary like input string to initialize global kernel parameters')
    parser.add_argument('--print',  type=int,   dest='printlevel', default=0,                  help='printlevel')
    parser.add_argument('--eta',    type=float, dest='eta',   default=defaults.etaarr,   nargs='+', help='eta array')
    parser.add_argument('--sigma',  type=float, dest='sigma', default=defaults.sigmaarr, nargs='+', help='sigma array')
    parser.add_argument('--ll',   action='store_true', dest='ll',       default=False,  help='if correct for the numper of threads')
    parser.add_argument('--save',   action='store_true', dest='save_all',       default=False,  help='if saving intermediate results in .npy file')
    parser.add_argument('--ada',  action='store_true', dest='adaptive', default=False,  help='if adapt sigma')
    parser.add_argument('--readkernel', action='store_true', dest='readk', default=False,  help='if X is kernel')
    parser.add_argument('--name',      type=str,   dest='nameout',       required=True, help='the name of the output file')
    parser.add_argument('--train_idx',      type=str,   dest='train_idx',       required=True, help='a txt file containing the training set indices of the  representations')
    parser.add_argument('--test_idx',      type=str,   dest='test_idx',       required=True, help='a txt file containing the test set indices of the  representations')
    
    args = parser.parse_args()
    
    if(args.readk): args.sigma = [np.nan]
    if(args.ll): correct_num_threads()
    
    print(vars(args))

    X = np.load(args.repr)
    y = np.loadtxt(args.prop)
    
    train_idx = np.loadtxt(args.train_idx, dtype=int)
    test_idx = np.loadtxt(args.test_idx, dtype=int)

    print(f"Number of training samples: {len(train_idx)}, Number of test samples: {len(test_idx)}")
    
    idx_test=list(test_idx)
    idx_train=list(train_idx)

    errors = hyperparameters(X[train_idx], y[train_idx], read_kernel=args.readk, sigma=args.sigma, eta=args.eta, akernel=args.akernel, splits=5, printlevel=args.printlevel, adaptive=args.adaptive)
    errors = np.array(errors)
    mae, stdev, eta, sigma = zip(*errors)

    print(errors[-1])
    aes, pred = final_error(X, y, sigma=sigma[-1], eta=eta[-1], idx_test=idx_test, idx_train=idx_train,
                            akernel=args.akernel, return_pred=True)
    # Uncomment to save predictions and absolute errors
    #np.save(f"{args.nameout}_pred", pred)        
    #np.save(f"{args.nameout}_absolute_errors", aes)
        
    with open(f"{args.nameout}.txt", "w") as f:
        f.write(f"{np.mean(aes)}\n")         

if __name__ == '__main__' : main()
