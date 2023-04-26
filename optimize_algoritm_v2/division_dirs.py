from optimize_algoritm_v2.func_getting import vector_weights, pose_weights, gender_weights, age_weights, func
from optimize_algoritm_v2.generation_sets import GenerateSets
import numpy as np
import os
import shutil
import pickle
from numpy import random


class DivisionDirs(GenerateSets):
    def __init__(self, input_path, output_path):
        super().__init__(input_path=input_path, output_path=output_path)
        self.make_dirs()
        with open(self.output_path + '/statistic.pkl', 'wb') as f:
            pickle.dump(self.statistic_dirs(), f)

    def make_dirs(self):
        title_dir = 'division_dirs'
        try:
            os.mkdir(self.output_path + '/' + title_dir)
        except:
            title_dir = 'division_dirs{}'.format(random.randint(1, 20))
            os.mkdir(self.output_path + '/' + title_dir)

        for key in self.dirs.keys():
            os.mkdir(self.output_path + '/' + title_dir + '/{}'.format(key))
            for image in self.dirs[key]:
                src = self.input_path + '/' + image
                dst = self.output_path + '/' + title_dir + '/{}/{}'.format(key, image)
                shutil.copyfile(src=src, dst=dst)

    def statistic_dirs(self):

        statistic = {}

        for idx, key in enumerate(self.dirs.keys()):
            array_gender = np.array([self.vector[img][643] for img in self.dirs[key]]).astype(float)
            array_age = np.array([self.vector[img][644] for img in self.dirs[key]]).astype(float)
            array_pose = np.array([np.array(self.vector[img][640:643]).astype(float) for img in self.dirs[key]])

            vector = max([np.array(self.compare[k].loc[lambda x: x < 0.6]) for k in self.dirs[key]], key=len)

            confidence = vector_weights(np.mean(vector)) * 0.5 + \
                         pose_weights(array_pose) * 0.2 + \
                         gender_weights(array_gender[~(np.isnan(array_gender))]) * 0.2 + \
                         age_weights(array_age[~(np.isnan(array_age))]) * 0.1

            statistic[f'dir{idx}'] = (
                {'confidence': confidence}, {'count_images': len(vector)}, {'title images': np.array(self.dirs[key])},
                {'threshold': np.around(vector, 2), 'mean_threshold': np.around(np.mean(vector), 2),
                 'median_threshold': np.around(np.median(vector), 2)},
                {'pose': np.array([i for i in map(func, array_pose)]),
                 'mean_rotate_up_down': np.around(np.mean(np.abs([array[0] for array in array_pose])), 0),
                 'mean_rotate_left_right': np.around(np.mean(np.abs([array[1] for array in array_pose])), 0),
                 'mean_slat_left_right': np.around(np.mean(np.abs([array[2] for array in array_pose])), 0)},
                {'gender': array_gender, 'gender_unique': np.unique(array_gender)},
                {'age': array_age, 'mean_age': np.mean(array_age[~(np.isnan(array_age))]),
                 'median_age': np.median(array_age[~(np.isnan(array_age))]),
                 'std_age': np.around(np.std(array_age[~(np.isnan(array_age))]), 0)}
            )

        return statistic
