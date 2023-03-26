import insightface as inf
import face_recognition as fr
import cv2 as cv
import numpy as np


class Image2Vector:

    def bbox_detection(self, image):
        img = cv.imread(image)
        app = inf.app.FaceAnalysis('buffalo_l', providers=['CUDAExecutionProvider', 'CPUExecutionProvider'])
        app.prepare(ctx_id=1, det_size=(256, 256))
        detect = app.get(img)
        if detect:
            return detect[0]['bbox']
        else:
            return np.array([0, 0, 0, 0])

    def get_embedding_face(self, image):
        img = cv.imread(image)
        app = inf.app.FaceAnalysis('buffalo_l', providers=['CUDAExecutionProvider', 'CPUExecutionProvider'])
        app.prepare(ctx_id=1, det_size=(256, 256))
        try:
            detect = app.get(img)
            return detect[0]['embedding']
        except:
            print('Not detection')
            return np.full(512, 999)

    def get_embedding_face_recognition(self, image):
        img = cv.imread(image)
        img = cv.resize(img, dsize=(256, 256))
        embedding = fr.face_encodings(img, model='cnn')
        try:
            return embedding[0]
        except:
            return np.full(128, 999)