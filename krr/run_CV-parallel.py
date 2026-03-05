#!/usr/bin/env python3
import os
import sys
import numpy as np
import qstack.regression.hyperparameters as hypers
import qstack.regression.regression as regress
import qstack.spahm.rho.utils as qutils
from qstack.regression.kernel_utils import defaults, train_test_split_idx
import sklearn
import joblib

def get_parameters_list(kernels, etas, sigmas, seeds):
    parameters = []
    for k in kernels:
        for e in etas:
            for s in sigmas:
                for seed in seeds:
                    parameters.append((seed,k,s,e))
    return parameters

seeds = range(10)

def cv_parallel(reps, targets, ncalls, nthreads, nameout, debug=False):
    def run_search(seed, kernel, sigma, eta, nthreads):
        idx_train, _, y_train, _ = train_test_split_idx(y=targets, test_size=int(0.1*len(targets)), random_state=seed)
        #K = np.exp((-1*distances[kernel][np.ix_(idx_train,idx_train)]/sigma))
        kernel_metric = {"G": "rbf", "myLfast": "laplacian"}
        #with parallel_backend("dask", n_jobs=1, inner_max_num_threads=20):
        K = sklearn.metrics.pairwise.pairwise_kernels(reps[idx_train], metric=kernel_metric[kernel], gamma=(1.0/sigma), n_jobs=nthreads)
        mae, std = hypers.k_fold_opt(K, eta, splits=5, read_kernel=True, y_train=y_train)
        #print(seed, kernel, eta, sigma, mae, std, file=fout, flush=True)
        return seed, kernel, eta, sigma, mae, std
    
    params = get_parameters_list(["G", "myLfast"], defaults.etaarr, defaults.sigmaarr, seeds)
    
    if debug:
        params = params[:ncalls]
    
    #print(*params, sep="\n")
    print(f"Running : {len(params)} parameter-runs.")
    
    seed_dict = {e:[] for e in seeds}
    print(joblib.cpu_count())
    
    with joblib.parallel_config(backend="loky", inner_max_num_threads=nthreads):
         results = joblib.Parallel(verbose=3, n_jobs=ncalls, return_as="list")(
            joblib.delayed(run_search)(*p, nthreads) for p in params)
    
    for seed, kernel, eta, sigma, mae, std in results:
        seed_dict[seed].append((mae, std, kernel, sigma, eta))
    
    lcs = []
    best_parameters = ["best parameters per split (e.g. i_split : [MAE, STD, KERNEL, SIGMA, ETA])"]
    predictions = []
    for s, a in seed_dict.items():
        if len(a) == 0:
            continue
        arr = np.array(a)
        best = np.nanargmin(arr[:,0])
        mae, std, kernel, sigma, eta = arr[best]
        lc, (targs, preds) = regress.regression(reps, targets, sigma=float(sigma), eta=float(eta), akernel=kernel, test_size=0.1, n_rep=1, random_state=s, save_pred=True)
        lcs.append(lc)
        predictions.append((targs, preds))
        best_parameters.append(f"{s} : {arr[best]}")
        print(f"{s} : {arr[best]}")

    np.save(f"{nameout}_hyper-search_results.npy", np.array(list(seed_dict.values()), dtype=object))
    
    lcs = np.array(lcs)
    np.save(f"{nameout}_best_LCs.npy", lcs)

    predictions = np.vstack(predictions).T
    
    lc = np.array([np.mean(lcs[:,:,0], axis=0), np.mean(lcs[:,:,1], axis=0), np.std(lcs[:,:,1], axis=0)])
    return lc.T, best_parameters, predictions

def run_single_lc(hyper_dict, reps, targets):
    lcs = []
    predictions = []
    best_parameters = ["best parameters per split (e.g. i_split : [MAE, STD, KERNEL, SIGMA, ETA])"]
    for s, a in hyper_dict.items():
        if len(a) == 0:
            continue
        arr = np.array(a)
        best = np.nanargmin(arr[:,0])
        mae, std, kernel, sigma, eta = arr[best]
        lc, (targs, preds) = regress.regression(reps, targets, sigma=float(sigma), eta=float(eta), akernel=kernel, test_size=0.2, n_rep=1, random_state=s, save_pred=True)
        predictions.append((targs, preds))
        lcs.append(lc)
        best_parameters.append(f"{s} : {arr[best]}")
        print(f"{s} : {arr[best]}")
    
    lcs = np.array(lcs)
    predictions = np.vstack(predictions).T
    #np.save(f"{nameout}_best_LCs.npy", lcs)
    
    lc = np.array([np.mean(lcs[:,:,0], axis=0), np.mean(lcs[:,:,1], axis=0), np.std(lcs[:,:,1], axis=0)])
    return lc.T, best_parameters, predictions


all_reps = ["spahm-a", "spahm-b", "slatm", "spahm-a-global", "spahm-b-global", "spahm-e"]
all_levels = ["neutral", "vertical", "relaxed"]



def main():
    import argparse
    parser = argparse.ArgumentParser(description="This script runs CV-LC with hyperparameter optimization in parallel.")
    parser.add_argument("--prop", required=True, type=str,  help="selects the tagret file")
    parser.add_argument("--rep", required=True,  help="the selected representation")
    parser.add_argument("--out", required=False, type=str,  default=None, help="directory to save the outptu files")
    parser.add_argument("--nproc", required=False, type=int, default=1, help="number of parallel processes spanned by `joblib`")
    parser.add_argument("--nthreads", required=False, type=int, default=1, help="number of maximum threads spanned by each process")
    parser.add_argument("--debug", required=False, action="store_true", help="enables debug run where iteration=nproc")
    parser.add_argument("--best", required=False, action="store_true", help="load hyper-parmeters results and runs a single time with best parameters (saves only average LC)")

    args=parser.parse_args()
    print(vars(args))

    reps = np.load(args.rep)

    Y_file = args.prop
    targets = np.loadtxt(Y_file, dtype=float)

    dirout = args.out if args.out is not None else os.getcwd()
    if not os.path.isdir(dirout): os.makedirs(dirout)
    nameout='_'.join(['LC', os.path.basename(args.rep), os.path.basename(args.prop)])
    nameout = os.path.join(dirout, nameout)
    
    ncalls = args.nproc
    nthreads = args.nthreads

    if args.best:
        print("Loading hyper-parameter search results and running LCs for best parameters only:")
        hyper_file = f"{nameout}_hyper-search_results.npy"
        hyper_results = np.load(hyper_file, allow_pickle=True)
        hyper_dict = { s:res for s, res in zip(seeds, hyper_results)}
        lc, header_line, predictions = run_single_lc(hyper_dict, reps, targets)
        header_line.append("Averaged LC (TRAINING_SIZE, MAEs, STDs)")
        np.savetxt(f"{nameout}_CV_LC.txt", lc, header="\n".join(header_line))
        np.savetxt(f"{nameout}_predictions.txt", predictions, header=f"{len(seeds)} X [targets, predictions]")
    else:
        lc, header_line, predictions = cv_parallel(reps, targets, ncalls, nthreads, nameout, debug=args.debug)
        header_line.append("Averaged LC (TRAINING_SIZE, MAEs, STDs)")
        print(lc)
        np.savetxt(f"{nameout}_CV_LC.txt", lc, header="\n".join(header_line))
        np.savetxt(f"{nameout}_predictions.txt", predictions, header=f"{len(seeds)} X [targets, predictions]")
        return 0

if __name__ == '__main__':
    main()




