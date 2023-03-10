import pytest
from module_compare.compare import CompareVector
import numpy as np


class TestCompareVector:

    def test_compare_matrix(self):
        path = '/home/nikita/PycharmProjects/ProjectVKR/data/dataset'
        cv = CompareVector(path_dir=path)

        matrix = cv.get_matrix_compare()

        assert (matrix.shape == (22, 22))

    def test_compare_vector(self):
        path = '/home/nikita/PycharmProjects/ProjectVKR/data/dataset'
        cv = CompareVector(path_dir=path)

        image_vector = cv.get_image_vector()

        assert (len(image_vector.keys()) == 22)

    def test_cosine_metrics(self):
        path = '/home/nikita/PycharmProjects/ProjectVKR/data/dataset'
        cv = CompareVector(path_dir=path)
        vector1 = np.array([1, 2, 5])
        vector2 = np.array([3, 5, 6])
        cosine = cv.compare_vector_cosine(vector1, vector2)

        assert cosine == 0.0616630719852328

    def test_euclidean_metrics(self):
        path = '/home/nikita/PycharmProjects/ProjectVKR/data/dataset'
        cv = CompareVector(path_dir=path)
        vector1 = np.array([1, 2, 5])
        vector2 = np.array([3, 5, 6])
        euclidean = cv.compare_vector_euclidean(vector1, vector2)

        assert np.around(euclidean, 3) == 3.742

    def test_same_people_image(self):
        path = '/home/nikita/PycharmProjects/ProjectVKR/data/dataset'
        cv = CompareVector(path_dir=path)
        image1 = cv.dict_vector[cv.image_title[0]]
        image2 = cv.dict_vector[cv.image_title[7]]

        vector = cv.compare_vector_cosine(image1, image2)

        assert vector > 0.6

    def test_diffrent_people_image(self):
        path = '/home/nikita/PycharmProjects/ProjectVKR/data/dataset'
        cv = CompareVector(path_dir=path)
        image1 = cv.dict_vector[cv.image_title[1]]
        image2 = cv.dict_vector[cv.image_title[9]]
        #print(cv.image_title)

        vector = cv.compare_vector_cosine(image1, image2)

        assert vector <= 0.6