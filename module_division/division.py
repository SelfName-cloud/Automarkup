import numpy as np
from module_compare.compare import CompareVector
import shutil
import os
import pickle
import random


class DivisionDirs(CompareVector):
    def __init__(self, path_dir_input, path_dir_output):
        super().__init__(path_dir=path_dir_input)
        self.path_dir_output = path_dir_output
        self.dict_dir = self.get_dir_division()
        with open(path_dir_output + '/dict_dir.pkl', 'wb') as f:
            pickle.dump(self.dict_dir, f)

    def get_dir_division(self) -> dict:
        dict_dir = {}
        array = []
        for idx, image in enumerate(self.matrix.index):
            if image in array:
                continue
            else:
                arr = np.array(self.matrix.iloc[idx].loc[lambda x: x == 1].index)
                array.extend(arr)
                dict_dir['dir{}'.format(idx)] = arr
        return dict_dir

    def make_new_dir(self) -> None:
        title_dir = 'division_dirs'
        try:
            os.mkdir(self.path_dir_output + '/' + title_dir)
        except:
            title_dir = 'division_dirs{}'.format(random.randint(1, 20))
            os.mkdir(self.path_dir_output + '/' + title_dir)

        for key, value in self.dict_dir.items():
            os.mkdir(self.path_dir_output + '/' + title_dir + '/{}'.format(key))
            for image in value:
                src = self.path_dir + '/' + image
                dst = self.path_dir_output + '/' + title_dir + '/{}/{}'.format(key, image)
                shutil.copyfile(src=src, dst=dst)
