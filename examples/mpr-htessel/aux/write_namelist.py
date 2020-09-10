import numpy as np
import f90nml as nml
import re
import os
import glob
import copy
from shutil import copyfile, copytree
import pickle
from mpr_namelist import MPRNameList
from htessel_namelist import HTESSELNameList

working_dir = './examples/mpr-htessel'
if working_dir[-1] != '/':
    working_dir += '/'


def get_last_iteration(working_directory):
    iter_directories = [s for s in os.listdir(working_directory) if s.find('iter_') != -1]
    nums = [int(re.findall('iter_(\d+)', s)[0]) for s in iter_directories]
    return max(nums)


def get_last_iter_folder_name(working_dir):
    return f'iter_{str(get_last_iteration(working_dir))}/'


def get_scaled_param_matrix_filename(working_dir, iter_folder):
    return glob.glob(f'{working_dir + iter_folder}/parameter_sets_1_scaled*.dat')[0]


def generate_nml(nmlist, param_map):
    nm = copy.deepcopy(nmlist)
    for k, v in param_map.items():
        path = find_namelist_item_path(nmlist, k)
        nm[path[0]][path[1]] = v
    nm.uppercase = True
    return nm


def param_set_split(param_set, param_partition):
    param_mpr = {}
    param_htessel = {}

    for param in param_set:
        if param_partition[param] == 'mpr':
            param_mpr[param] = param_set[param]
        elif param_partition[param] == 'htessel':
            param_htessel[param] = param_set[param]

    return param_mpr, param_htessel


def write_namelists(working_dir):

    iter_folder = get_last_iter_folder_name(working_dir)
    print(f'Working the the last iteration folder "{iter_folder}"\n')
    scaled_param_matrix_filename = get_scaled_param_matrix_filename(working_dir, iter_folder)
    print(f'Openning the scaled parameters file "{scaled_param_matrix_filename}"')

    M = open(scaled_param_matrix_filename).readlines()
    param = open(f'{working_dir}/parameters.dat').readlines()
    param_partition = pickle.load(open(f'{working_dir}/parameters_partition.pkl', 'rb'))

    num_header_lines = int(re.findall(r'\d+', M[0])[0])
    print(f'number of header lines in {scaled_param_matrix_filename} to skip is {num_header_lines}')
    morris_params = M[num_header_lines : ]

    param_ids = [re.findall('(x_{\d+})', x)[0] for x in param[2: ]]
    param_names = [re.findall('# (.+)$', x)[0] for x in param[2: ]]

    num_digits = int(np.log10(len(morris_params))) + 1
    digit_format = f'0{num_digits}'

    mpr_global_nmlist = nml.read(f'{working_dir}/default_sim/mpr_global_parameter.nml')
    htessel_nmlist = nml.read(f'{working_dir}/default_sim/input')

    # loop over all the rows of the morris matrix
    for i, morris_set in enumerate(morris_params):
        new_params = {k: float(v) for k, v in zip(param_names, morris_set.split())}
        param_mpr, param_htessel = param_set_split(new_params, param_partition)

        sim_folder = f'sim_{i+1:{digit_format}}'
        copytree("../default_sim", sim_folder)
        # copy the default_sim folder into the new folder
        os.chdir(sim_folder)

        # loop over htessel and mpr parameters and their new lists
        for params, nmlist in zip([param_mpr, param_htessel],
                                  [MPRNameList(copy.deepcopy(mpr_global_nmlist)),
                                   HTESSELNameList(copy.deepcopy(htessel_nmlist))]):
            nmlist.read_only = False

            # set the parameters values
            for k, v in params.items():
                nmlist[k] = v

            nmlist.nml.write(nmlist.tag, force=True)


        os.chdir('..')

