#!/usr/bin/env python

#SBATCH --time=00:01:00
#SBATCH --output=LOG.exp.icon-lam_nwp1nest.run.%j.o
#SBATCH --error=LOG.exp.icon-lam_nwp1nest.run.%j.o
#SBATCH --partition=batch
#SBATCH --account=mhmopti


from subprocess import Popen, PIPE
import multiprocessing as mp
import os


def is_empty(file_name):
    return os.path.getsize(file_name) == 0


def run_program(folder):
    os.chdir(folder)
    p = Popen(['./script'], stdout=open('output', 'w'), stderr=open('error', 'w')).communicate()
    
    if is_empty('error'):
        print(f'running case {folder} was successful')
    else:
        print(f'running case {folder} failed')
        
    os.chdir('..')
    

subfolder_names = [f'folder_{i:02}' for i in range(1, 25)]
pool = mp.Pool(processes=8)
pool.map(run_program, subfolder_names)
