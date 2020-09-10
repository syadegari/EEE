import sys
import os
import re
path = re.findall('^.+examples/mpr-htessel', os.getcwd())[0]
sys.path.insert(1, path + '/aux')
from write_namelist import write_namelists

print(f'current working directory: {os.getcwd()}')
write_namelists('../')