from optimize_algoritm_v2.func_getting import get_insightface_embedding, get_face_recognition_embedding, get_metrics
import numpy as np
import pandas as pd
import os


class ExtractDataFromImage:
    def __init__(self, input_path, output_path):
        self.input_path = input_path
        self.output_path = output_path
        self.title_images = os.listdir(self.input_path)
        self.count_image = len(self.title_images)

        self.path_to_vector_file = self.output_path + '/vector.h5'
        self.path_to_compare_file = self.output_path + '/compare.h5'
        self.path_to_dirs_file = self.output_path + '/dirs.h5'

        with open(self.path_to_vector_file, 'wb') as f:
            f.close()

        self.vector = pd.HDFStore(self.path_to_vector_file, mode='r+')
        self.extract_data()

    def extract_data(self):

        for idx, img in enumerate(self.title_images):
            inf_data = get_insightface_embedding(self.input_path + '/' + img)
            fr_data = get_face_recognition_embedding(self.input_path + '/' + img)

            self.vector[img] = pd.Series(np.concatenate(
                (inf_data['embedding'].astype(float),
                fr_data.astype(float),
                inf_data['pose'].astype(float),
                np.array([inf_data['gender'],
                          inf_data['age']])), axis=0))



