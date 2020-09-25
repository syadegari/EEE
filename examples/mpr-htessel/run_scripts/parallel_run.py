#!/usr/bin/env python

#SBATCH --time=00:35:00
#SBATCH --output=LOG.exp.icon-lam_nwp1nest.run.%j.o
#SBATCH --error=LOG.exp.icon-lam_nwp1nest.run.%j.o
#SBATCH --partition=batch
#SBATCH --account=mhmopti


from subprocess import Popen, PIPE
import multiprocessing as mp
import os


def is_empty(file_name):
    return os.path.getsize(file_name) == 0


def run_program(folder, num_threads=8):
    os.chdir(folder)
    my_env = os.environ.copy()
    my_env['OMP_NUM_THREADS'] = str(num_threads)
    p = Popen('./run_programs', shell=True,
              stdout=open('output', 'w'),
              stderr=open('error', 'w'), env=my_env).communicate()
    os.chdir('..')



subfolder_names = [x[0] for x in os.walk('.') if x[0].find('sim_') != -1]
pool = mp.Pool(processes=10)
pool.map(run_program, subfolder_names)
