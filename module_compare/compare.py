import numpy as np
import pandas as pd
import os
import glob
from module_image_working.detection import Image2Vector
from scipy.spatial.distance import pdist


class CompareVector:
    def __init__(self, path_dir):
        self.path_dir = path_dir
        self.paths = glob.glob(path_dir + '/*.jpg')
        self.length = len(self.paths)
        self.image_title = [title.split('/')[-1] for title in self.paths]
        self.get_face_vector = Image2Vector()
        self.dict_vector = self.get_image_vector()
        self.matrix = self.get_matrix_compare()

    def get_image_vector(self) -> dict:
        dict_vector = {}
        directory = os.fsencode(self.path_dir)
        for img in os.listdir(directory):
            img_name = os.fsdecode(img)
            print(img_name)
            dict_vector[img_name] = self.get_face_vector.get_embedding_face((self.path_dir + '/' + img_name))
        return dict_vector

    @staticmethod
    def compare_vector_euclidean(vector1, vector2) -> float:
        euclidean = pdist([vector1, vector2], 'euclidean')
        return float(euclidean)

    @staticmethod
    def compare_vector_cosine(vector1, vector2) -> float:
        cosine = pdist([vector1, vector2], 'cosine')
        return float(cosine)

    def get_euclidean_metric(self, image1, image2) -> float:
        vector1 = self.dict_vector[image1]
        vector2 = self.dict_vector[image2]
        return self.compare_vector_euclidean(vector1, vector2)

    def get_cosine_metric(self, image1, image2) -> float:
        vector1 = self.dict_vector[image1]
        vector2 = self.dict_vector[image2]
        return self.compare_vector_cosine(vector1, vector2)

    def get_matrix_compare(self) -> pd.DataFrame:
        matrix = np.empty((self.length, self.length,))
        matrix[:] = np.nan

        for idx_row in range(self.length):
            for idx_column in range(idx_row, self.length):
                matrix[idx_row, idx_column] = self.get_cosine_metric(self.image_title[idx_row],
                                                                     self.image_title[idx_column])

        matrix = np.where(matrix <= 0.6, 1, 0)
        matrix = pd.DataFrame(matrix, index=self.image_title, columns=self.image_title)
        matrix = (matrix + matrix.T) - np.diag(np.full(self.length, 1))

        return matrix



















































































