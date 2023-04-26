from optimize_algoritm_v2.extract_data import ExtractDataFromImage
from optimize_algoritm_v2.func_getting import get_metrics
import pandas as pd
import numpy as np


class GenerateSets(ExtractDataFromImage):
    def __init__(self, input_path, output_path):
        super().__init__(input_path=input_path, output_path=output_path)

        self.keys = self.vector.keys()
        self.length = len(self.keys)

        with open(self.path_to_compare_file, 'wb') as compare_file:
            compare_file.close()

        self.compare = pd.HDFStore(self.path_to_compare_file, mode='r+')

        self.get_all_sets()

        self.candidates = [list(self.compare[key].loc[lambda x: x <= 0.6].index) for key in self.keys]

        with open(self.path_to_dirs_file, 'wb') as dirs_file:
            dirs_file.close()

        self.dirs = pd.HDFStore(self.path_to_dirs_file, mode='r+')

        self.find_cover_dirs(self.candidates)

    def get_all_sets(self):

        for idx_row in range(self.length):

            array = []

            array_title = []

            for idx_column in range(idx_row, self.length):

                if self.vector[self.keys[idx_row]][513] != np.nan and self.vector[self.keys[idx_column]][513] != np.nan:

                    metric_fr = get_metrics(self.vector[self.keys[idx_row]][512:640],
                                            self.vector[self.keys[idx_column]][512:640],
                                            dist='euclidean')
                    metric_inf = get_metrics(self.vector[self.keys[idx_row]][:512],
                                             self.vector[self.keys[idx_column]][:512],
                                             dist='cosine')

                    array.append((metric_fr + metric_inf) / 2)

                else:

                    array.append(get_metrics(self.vector[self.keys[idx_row]][:512],
                                             self.vector[self.keys[idx_column]][:512],
                                             dist='cosine'))

                array_title.append(self.keys[idx_column])

            self.compare[self.keys[idx_row]] = pd.Series(data=array, index=array_title)

    def find_cover_dirs(self, candidates):

        remaining_elements = set(sum(candidates, []))

        for idx, candidate in enumerate(sorted(candidates, key=len, reverse=True)):
            if not remaining_elements.isdisjoint(candidate):

                self.dirs[f'dir{idx}'] = pd.Series(np.array(candidate))

                remaining_elements.difference_update(candidate)

                if not remaining_elements:
                    break








