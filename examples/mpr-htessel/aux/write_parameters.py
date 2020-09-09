import f90nml as nml
import numpy as np
from mask import ParamMask
import pickle
import shutil
import f90nml as nml
from htessel_namelist import HTESSELNameList
from mpr_namelist import MPRNameList


def merge_dict(dict1: dict, dict2: dict) -> dict:
    d = {}
    d.update(dict1)
    d.update(dict2)
    return d


def write_paramset_uniform(f, pos, low, high, default, param_name, param_format):
    pos_tag = "x_{" + f"{pos:{param_format}}" + f"}}   uniform  {low: .8e}   {high: .8e}   {default: .8e}   1 # {param_name}\n"
    f.write(pos_tag)



def write_parameters(sim_folder, htessel_mask, mpr_mask):

    htessel_mask = ParamMask(f'{sim_folder}/{htessel_mask}',
                             HTESSELNameList(nml.read(f'{sim_folder}/default_sim/input'))).get_mask()
    mpr_mask = ParamMask(f'{sim_folder}/{mpr_mask}',
                         MPRNameList(nml.read(f'{sim_folder}/default_sim/mpr_global_parameter.nml'))).get_mask()

    mask = merge_dict(htessel_mask, mpr_mask)
    mask_partition = merge_dict({par_name: 'mpr' for par_name in mpr_mask},
                                {par_name: 'htessel' for par_name in htessel_mask})
    pickle.dump(mask_partition, open(f'{sim_folder}/parameters_partition.pkl', 'wb'))

    num_params = len(mpr_mask) + len(htessel_mask)
    num_digits = int(np.log10(num_params)) + 1
    param_format_number = f'0{num_digits}'


    f = open(f'{sim_folder}/parameters.dat', 'w')
    f.write(
        '# para   dist       lower     upper     default   informative(0)_or_noninformative(1)_or_ignored(-1)    # comment\n#                   mean      stddev\n')

    ipos = 1
    for param_name in mask:
        low = mask[param_name]['min']
        high = mask[param_name]['max']
        default = mask[param_name]['default']
        write_paramset_uniform(f, ipos, low, high, default, param_name, param_format_number)
        ipos += 1
    f.close()
