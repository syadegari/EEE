#!/usr/bin/env python

#SBATCH --time=00:25:00
#SBATCH --output=LOG.exp.icon-lam_nwp1nest.run.%j.o
#SBATCH --error=LOG.exp.icon-lam_nwp1nest.run.%j.o
#SBATCH --partition=batch
#SBATCH --account=mhmopti


import matplotlib.pyplot as plt
import numpy as np
from subprocess import Popen
import os
import time


def is_empty(file_name):
    return os.path.getsize(file_name) == 0


def finished_with_succes(file_name):
    return open(file_name, 'r').readlines()[-1].find('MASTER1s: Time total:') != -1


def time_runs(executable, folder, threads=[4, 8, 16, 24, 32, 64], nloop=5):
    os.chdir(folder)
    timer = {i: [] for i in threads}
    for i in range(nloop):
        for omp_num_threads in threads:

            my_env = os.environ.copy()
            my_env['OMP_NUM_THREADS'] = str(omp_num_threads)

            outfile = f'output_thr{omp_num_threads}_nloop{i+1}'
            errfile = f'error_thr{omp_num_threads}_nloop{i+1}'
            
            t1 = time.time()
            Popen(executable, shell=True,
                  stdout=open(outfile, 'w'),
                  stderr=open(errfile, 'w'), env=my_env).communicate()
            t2 = time.time()
            
            if finished_with_succes(outfile):
                timer[omp_num_threads].append(t2 - t1)
    os.chdir('..')
    return timer


def plot(d):
    plt.style.use('seaborn-whitegrid')
    fig, ax = plt.subplots()

    ax.errorbar(
        x = [str(x) for x in list(d.keys())],
        y = [np.mean(v) for v in [d[k] if d[k] !=[] else np.nan for k in d]],
        yerr=[np.std(v) for v in [d[k] if d[k] != [] else np.nan for k in d]],
        fmt='.k',
        capsize=8,
        markersize=18,
        elinewidth=5,
        ecolor='darkgray'
    )
    ax.set_xlabel('#threads')
    ax.set_ylabel('seconds')

    fig.savefig('scale_plots.png')


d = time_runs('./run_programs', 'sim_timing',
              threads=[4, 8, 12, 16, 24, 32, 48, 64],
              nloop=5)

for k, v in d.items():
    print(f'Threads = {k}')
    print(v)
    
plot(d)
