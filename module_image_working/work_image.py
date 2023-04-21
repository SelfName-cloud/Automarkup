import face_recognition
import insightface
import numpy as np
#from deepface import DeepFace
import cv2 as cv


def get_insightface_embedding(image):
    image = cv.imread(image)
    app = insightface.app.FaceAnalysis(name='buffalo_l', providers=['CUDAExecutionProvider'])
    try:
        app.prepare(ctx_id=0, det_size=(256, 256))
        detect = app.get(img=image)
        return detect[0]
    except:
        response_dict = {
            'pose': np.array([999, 999, 999]),
            'gender': np.nan,
            'age': np.nan,
            'embedding': np.full(512, 999)
        }
        return response_dict

"""
def get_deepface_analyze(image):
    try:
        analyze = DeepFace.analyze(img_path=image, actions=['race'], detector_backend='ssd')
        return analyze[0]
    except:
        return {'dominant_race': np.nan}"""


def get_face_recognition_embedding(image):
    image = cv.imread(image)
    try:
        embedding = face_recognition.face_encodings(face_image=image)
        return np.array(embedding)
    except:
        return np.full(128, np.nan)

