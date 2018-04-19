import os
import cv2
import numpy as np
from PIL import Image
from flask import jsonify

recognizer = cv2.face.LBPHFaceRecognizer_create()
path = 'dataset'


def train_data():
    if not os.path.exists('./recognizer'):
        os.makedirs('./recognizer')
    ids, faces = get_image_with_id(path)
    recognizer.train(faces, ids)
    recognizer.save('recognizer/trainingData.yml')
    cv2.destroyAllWindows()
    return jsonify({"status": "SUCCESS"})


def get_image_with_id(path):
    imagePaths = [os.path.join(path, f) for f in os.listdir(path)]
    faces = []
    IDs = []
    for imagePath in imagePaths:
        faceImg = Image.open(imagePath).convert('L')
        faceNp = np.array(faceImg, 'uint8')
        ID = int(os.path.split(imagePath)[-1].split('.')[1])
        faces.append(faceNp)
        IDs.append(ID)
        cv2.waitKey(10)
    return np.array(IDs), faces
