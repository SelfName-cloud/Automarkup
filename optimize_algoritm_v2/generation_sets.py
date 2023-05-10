from optimize_algoritm_v2.extract_data import ExtractDataFromImage
from optimize_algoritm_v2.func_getting import get_metrics
import pandas as pd
import numpy as np
import h5py


class GenerateSets(ExtractDataFromImage):
    def __init__(self, input_path, output_path):
        super().__init__(input_path=input_path, output_path=output_path)

        self.keys = list(self.vector.keys())
        self.length = len(self.keys)

        #with open(self.path_to_compare_file, 'wb') as compare_file:
        #    compare_file.close()

        #self.compare = pd.HDFStore(self.path_to_compare_file, mode='r+')
        self.compare = h5py.File(self.path_to_compare_file, mode='a')

        self.get_all_sets()

        self.candidates = [list(self.compare[key][:]) for key in self.keys]

        #with open(self.path_to_dirs_file, 'wb') as dirs_file:
        #    dirs_file.close()

        #self.dirs = pd.HDFStore(self.path_to_dirs_file, mode='r+')
        self.dirs = h5py.File(self.path_to_dirs_file, mode='a')

        self.find_cover_dirs(self.candidates)

    def get_all_sets(self):

        dt = h5py.special_dtype(vlen=str)

        for idx_row in range(self.length):

            #array = []

            #array_title = []

            temp_dict = {}

            for idx_column in range(idx_row, self.length):

                if self.vector[self.keys[idx_row]][513] != np.nan and self.vector[self.keys[idx_column]][513] != np.nan:

                    metric_fr = get_metrics(self.vector[self.keys[idx_row]][512:640],
                                            self.vector[self.keys[idx_column]][512:640],
                                            dist='euclidean')
                    metric_inf = get_metrics(self.vector[self.keys[idx_row]][:512],
                                             self.vector[self.keys[idx_column]][:512],
                                             dist='cosine')

                    #array.append((metric_fr + metric_inf) / 2)

                    temp_dict[self.keys[idx_column]] = (metric_fr + metric_inf) / 2

                else:

                    metric_fr = get_metrics(self.vector[self.keys[idx_row]][:512],
                                             self.vector[self.keys[idx_column]][:512],
                                             dist='cosine')

                    temp_dict[self.keys[idx_column]] = metric_fr

                #array_title.append(self.keys[idx_column])

            df = np.array(pd.Series(data=list(temp_dict.values()), index=list(temp_dict.keys())).loc[lambda x: x <= 0.6].index)

            #self.compare[self.keys[idx_row]]

            self.compare.create_dataset(name=self.keys[idx_row], shape=df.shape, dtype=dt, data=df)

            print('\r', 'Count set ', idx_row+1, '/', self.length, end='')

    def find_cover_dirs(self, candidates):

        dt = h5py.special_dtype(vlen=str)

        remaining_elements = set(sum(candidates, []))

        for idx, candidate in enumerate(sorted(candidates, key=len, reverse=True)):
            if not remaining_elements.isdisjoint(candidate):

                #self.dirs[f'dir{idx}'] = pd.Series()

                array = np.array(candidate)

                self.dirs.create_dataset(name=f'dir{idx}', shape=array.shape, dtype=dt, data=array)

                remaining_elements.difference_update(candidate)

                if not remaining_elements:
                    break








