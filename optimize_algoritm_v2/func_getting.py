import face_recognition
import insightface
import numpy as np
import cv2 as cv
from scipy.spatial.distance import pdist
import psutil


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


def get_face_recognition_embedding(image):
    image = cv.imread(image)
    try:
        embedding = face_recognition.face_encodings(face_image=image)[0]
        return np.array(embedding)
    except:
        return np.full(128, np.nan)


def get_metrics(vector1, vector2, dist='cosine'):
    metric = pdist([vector1, vector2], dist)
    return float(metric)


def check_memory():
    return psutil.virtual_memory().available / (1024 * 1024 * 1024)


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


def gender_weights(array):
    if len(np.unique(array)) == 1:
        return 100
    else:
        return 10


def race_weights(array):
    if len(np.unique(array)) == 1:
        return 100
    else:
        return 10


def age_weights(array):
    if np.std(array) < 15:
        return 100
    else:
        return 10


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


def func(array):
    deg = np.sum(np.abs(array))
    num = np.around((100 * deg) / 240, 0)
    return f'{num}%'