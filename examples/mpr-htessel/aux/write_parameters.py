import numpy as np
from mask import ParamMask
import pickle
import f90nml as nml
from htessel_namelist import HTESSELNameList
from mpr_namelist import MPRNameList
from util import merge_dict


def write_paramset_uniform(f, pos, low, high, default, param_name, param_format, flag):
    pos_tag = "x_{" + f"{pos:{param_format}}" + f"}}   uniform  {low: .8e}   {high: .8e}   {default: .8e}   {flag: 2} # {param_name}\n"
    f.write(pos_tag)


def write_parameters(sim_folder, htessel_mask, mpr_mask):

    htessel_namelist = HTESSELNameList(nml.read(f'{sim_folder}/default_sim/input'))
    mpr_namelist = MPRNameList(nml.read(f'{sim_folder}/default_sim/mpr_global_parameter.nml'))

    htessel_mask = ParamMask(f'{sim_folder}/{htessel_mask}', htessel_namelist).get_mask()
    mpr_mask = ParamMask(f'{sim_folder}/{mpr_mask}', mpr_namelist).get_mask()

    mask = merge_dict(htessel_mask, mpr_mask)

    # mask_partition = merge_dict({par_name: 'mpr' for par_name in mpr_mask},
    #                             {par_name: 'htessel' for par_name in htessel_mask})
    param_partition = merge_dict({par_name: 'mpr' for par_name in mpr_namelist.get_all_model_parameters()},
                                 {par_name: 'htessel' for par_name in htessel_namelist.get_all_model_parameters()})
    pickle.dump(param_partition, open(f'{sim_folder}/parameters_partition.pkl', 'wb'))

    num_params = len(mpr_namelist.get_all_model_parameters()) + len(htessel_namelist.get_all_model_parameters())
    num_digits = int(np.log10(num_params)) + 1
    param_format_number = f'0{num_digits}'

    f = open(f'{sim_folder}/parameters.dat', 'w')
    f.write('# para   dist       lower     upper     default   informative(0)_or_noninformative(1)_or_ignored(-1)    # comment\n#                   mean      stddev\n')
    ipos = 1
    for param_name in [*htessel_namelist.get_all_model_parameters(), *mpr_namelist.get_all_model_parameters()]:

        if param_name in mask:
            low = mask[param_name]['min']
            high = mask[param_name]['max']
            default = mask[param_name]['default']
            flag = 1
        else:
            low = 0.0
            high = 0.0
            default = 0.0
            flag = -1
        write_paramset_uniform(f, ipos, low, high, default, param_name, param_format_number, flag)
        ipos += 1
    f.close()
