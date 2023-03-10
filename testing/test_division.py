import pytest as pt
import numpy as np
from module_division.division import DivisionDirs


class TestDivisionDirs:

    def test_dir_division(self):
        input_dirs = '/home/nikita/PycharmProjects/ProjectVKR/data/dataset'
        output_dirs = 'home/nikita/project_VKR'
        dd = DivisionDirs(path_dir_input=input_dirs, path_dir_output=output_dirs)
        dirs = dd.get_dir_division()

        assert len(dirs.keys()) == 11