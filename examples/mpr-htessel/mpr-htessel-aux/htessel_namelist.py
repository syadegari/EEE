from abstract_namelist import AbstractNameList
from typing import List


class HTESSELNameList(AbstractNameList):

    def __init__(self, namelist):
        super(HTESSELNameList, self).__init__(namelist)
        self.tag = 'input'
        self.nml.uppercase = True

    def find(self, kw):
        for section_name in self.nml.keys():
            for subsection_name in self.nml[section_name]:
                if subsection_name == kw:
                    return [section_name, subsection_name]
        raise Exception(f'No {kw} where found in the given namelist file')

    def __getitem__(self, kw):
        path1, path2 = self.find(kw)
        return self.nml[path1][path2]

    def __setitem__(self, kw, value):
        if not self.read_only:
            path1, path2 = self.find(kw)
            self.nml[path1][path2] = value
        else:
            raise Exception(f'The namelist is readonly')

    def get_all_model_parameters(self) -> List[str]:
        l = []
        for name in self.nml.keys():
            if name.find('nampar') != -1:
                l.append(list(self.nml[name].keys()))
        return l