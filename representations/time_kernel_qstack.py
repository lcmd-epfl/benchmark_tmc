#!/bin/env python
import time
import numpy as np
import resource
import qstack.regression.kernel as regression

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

def kernel_builder(reps, kernel_type="G"):
    """
    Build a kernel from molecular representations.

    Args:
        reps (numpy.ndarray): 2D array of shape (n_molecules, n_features).
        kernel_type (str): Kernel type, "G" (Gaussian) or "L" (Laplacian).
            Default is "G".

    Returns:
        numpy.ndarray: Kernel matrix.
    """
    k = regression.kernel(reps, akernel=kernel_type, gkernel=None)
    return k

def main():
    import argparse
    parser = argparse.ArgumentParser(description="Construct the kernel and measure timings")
    parser.add_argument("--rep_file", required=True, type=str, help="Path to a .npy file of molecular representations")
    parser.add_argument("--akernel", required=True, type=str, help="Local kernel type: G (Gaussian) or L (Laplacian)")

    args = parser.parse_args()
    print(vars(args))

    reps = np.load(args.rep_file)
    
    start = time.perf_counter()
    kernel = kernel_builder(reps, kernel_type=args.akernel)
    stop = time.perf_counter()
    elapsed = stop - start
    print(f"Loaded representation file: {args.rep_file}")
    print(f"Representation shape: {reps.shape}")
    print(f"Kernel generation times ({args.akernel}): {elapsed}")

    return 0

if __name__ == '__main__':
    kernel_builder = unix_time_decorator(kernel_builder)
    main()


