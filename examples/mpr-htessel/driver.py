#!/usr/bin/env python

import argparse
import os
import sys
sys.path.insert(1, './aux')
from aux import write_parameters

parser = argparse.ArgumentParser()
# parser.add_argument('--check-default-simulation', action='store_true', help='')
parser.add_argument('--make-parameters', action='store_true', help='')
parser.add_argument('--htessel-mask', help='')
parser.add_argument('--mpr-mask', help='')

required_named = parser.add_argument_group('required named argument')
required_named.add_argument('--sim-folder', help='folder where the `default_sim` folder is situated')

args = parser.parse_args()


def get_default_sim_folder(sim_folder):
    if os.path.exists(sim_folder + '/default_sim'):
        return f'{sim_folder}/default_sim'
    else:
        raise Exception(f'default simulation folder "default_sim" is not found at {sim_folder}')


def check_inputs(default_sim_path):

    inputs = ['input',
              'mpr_global_parameter.nml',
              'mpr.nml']
    for name in inputs:
        assert os.path.exists(f'{default_sim_path}/{name}'), f"didn't find {name} in {default_sim_path}"


sim_folder = args.sim_folder
default_sim_folder = get_default_sim_folder(sim_folder)

if args.htessel_mask is not None:
    htessel_mask_name = args.htessel_mask
else:
    htessel_mask_name = ''

if args.mpr_mask is not None:
    mpr_mask_name = args.mpr_mask
else:
    mpr_mask_name = ''

check_inputs(default_sim_folder)
write_parameters.write_parameters(sim_folder, htessel_mask_name, mpr_mask_name)
