import numpy as np
import pandas as pd
from optimize_algorithm import work_image
from scipy.spatial.distance import pdist
from numpy import random
import psutil
import shutil
import os
import pickle


class Compare:
    def __init__(self, input_path, output_path):
        self.input_path = input_path
        print(self.input_path)
        self.output_path = output_path
        print(self.output_path)
        self.title_images = os.listdir(input_path)
        self.count_images = len(self.title_images)
        self.path_to_vector_file = self.output_path + '/vector.h5'
        self.path_to_compare_file = self.output_path + '/compare.h5'
        self.path_to_dirs_file = self.output_path + '/dirs.h5'
        with open(self.path_to_vector_file, 'wb') as vector_file:
            vector_file.close()
        with open(self.path_to_compare_file, 'wb') as compare_file:
            compare_file.close()
        with open(self.path_to_dirs_file, 'wb') as dirs_file:
            dirs_file.close()
        self.vector = pd.HDFStore(self.path_to_vector_file, mode='r+')
        self.compare = pd.HDFStore(self.path_to_compare_file, mode='r+')
        self.dirs = pd.HDFStore(self.path_to_dirs_file, mode='r+')
        self.find_compare_image()
        self.candidates = [list(self.compare[k].loc[lambda x: x < 0.6].index) for k in self.compare.keys()]
        self.find_cover_dirs(candidates=self.candidates)
        self.make_dirs()
        with open(self.output_path + '/statistic.pkl', 'wb') as f:
            pickle.dump(self.statistic_dirs(), f)

    @staticmethod
    def get_metrics(vector1, vector2, dist='euclidean'):
        metric = pdist([vector1, vector2], dist)
        return float(metric)

    @staticmethod
    def check_memory():
        return psutil.virtual_memory().available / (1024 * 1024 * 1024)

    def find_compare_image(self, alg_stacking=False):
        for idx, img in enumerate(self.title_images):
            embedding_insightface = work_image.get_insightface_embedding(self.input_path + '/' + img)
            #analyze = work_image.get_deepface_analyze(self.input_path + '/' + img)
            embedding_face_recognition = work_image.get_face_recognition_embedding(self.input_path + '/' + img)

            self.vector[img] = pd.Series(np.concatenate([embedding_insightface['embedding'],
                                                         embedding_face_recognition,
                                                         embedding_insightface['pose'],
                                                         np.array([embedding_insightface['gender'],
                                                                   embedding_insightface['age']])], axis=0))

            imgs_posted = self.vector.keys()

            array = []

            for img_post in imgs_posted:

                metric_vector1 = self.get_metrics(self.vector[img][:512], self.vector[img_post][:512], dist='cosine')

                array.append(metric_vector1)

            print(self.check_memory())
            self.compare[img] = pd.Series(data=np.array(array), index=imgs_posted)

    def find_cover_dirs(self, candidates):

        remaining_elements = set(sum(candidates, []))

        for idx, candidate in enumerate(sorted(candidates, key=len, reverse=True)):
            if not remaining_elements.isdisjoint(candidate):

                self.dirs[f'dir{idx}'] = pd.Series(np.array(candidate))

                remaining_elements.difference_update(candidate)

                if not remaining_elements:
                    break

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

    @staticmethod
    def vector_weights(n):
        if n > 0.5:
            return 10
        elif (n < 0.5) and (n > 0.4):
            return 30
        elif (n < 0.4) and (n > 0.3):
            return 60
        elif (n < 0.3) and (n > 0.2):
            return 80
        else:
            return 100

    @staticmethod
    def gender_weights(array):
        if len(np.unique(array)) == 1:
            return 100
        else:
            return 10

    @staticmethod
    def race_weights(array):
        if len(np.unique(array)) == 1:
            return 100
        else:
            return 10

    @staticmethod
    def age_weights(array):
        if np.std(array) < 15:
            return 100
        else:
            return 10

    @staticmethod
    def pose_weights(arrays):
        mean = np.mean([np.sum(np.abs(arr)) for arr in arrays])

        if mean < 15:
            return 100
        elif (mean < 30) and (mean > 15):
            return 80
        elif (mean < 45) and (mean > 30):
            return 60
        elif (mean < 60) and (mean > 45):
            return 40
        elif (mean < 90) and (mean > 60):
            return 20
        else:
            return 0

    @staticmethod
    def func(array):
        deg = np.sum(np.abs(array))
        num = np.around((100 * deg) / 240, 0)
        return f'{num}%'

    def statistic_dirs(self):

        statistic = {}

        for idx, key in enumerate(self.dirs.keys()):
            array_gender = np.array([self.vector[img][643] for img in self.dirs[key]]).astype(float)
            array_age = np.array([self.vector[img][644] for img in self.dirs[key]]).astype(float)
            array_pose = np.array([np.array(self.vector[img][640:643]).astype(float) for img in self.dirs[key]])

            vector = max([np.array(self.compare[k].loc[lambda x: x < 0.6]) for k in self.dirs[key]], key=len)

            confidence = self.vector_weights(np.mean(vector)) * 0.5 + \
                         self.pose_weights(array_pose) * 0.2 + \
                         self.gender_weights(array_gender[~(np.isnan(array_gender))]) * 0.2 + \
                         self.age_weights(array_age[~(np.isnan(array_age))])

            statistic[f'dir{idx}'] = (
                {'confidence': confidence}, {'count_images': len(vector)}, {'title images': np.array(self.dirs[key])},
                {'threshold': np.around(vector, 2), 'mean_threshold': np.around(np.mean(vector), 2),
                 'median_threshold': np.around(np.median(vector), 2)},
                {'pose': np.array([i for i in map(self.func, array_pose)]),
                 'mean_rotate_up_down': np.around(np.mean(np.abs([array[0] for array in array_pose])), 0),
                 'mean_rotate_left_right': np.around(np.mean(np.abs([array[1] for array in array_pose])), 0),
                 'mean_slat_left_right': np.around(np.mean(np.abs([array[2] for array in array_pose])), 0)},
                {'gender': array_gender, 'gender_unique': np.unique(array_gender)},
                {'age': array_age, 'mean_age': np.mean(array_age[~(np.isnan(array_age))]),
                 'median_age': np.median(array_age[~(np.isnan(array_age))]),
                 'std_age': np.around(np.std(array_age[~(np.isnan(array_age))]), 0)}

            )
        return statistic


if __name__ == '__main__':
    comp = Compare(input_path='/data/dataset', output_path='/home/nikita/data_markup')