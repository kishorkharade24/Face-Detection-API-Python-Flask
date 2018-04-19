import cv2
import numpy as np
import sqlite3
import os
import json
from flask import jsonify

# Constant
trainer = "recognizer/trainingData.yml"


def detect_faces(image):
    data = {}
    data["matches"] = []
    data["message"] = "No Records Found"
    connection = sqlite3.connect('database.db')
    c = connection.cursor()
    if not os.path.isfile(trainer):
        return "Please execute trainer first."
    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    img = cv2.imread(os.path.join("./data", image))
    os.system("rm -rf " + os.path.join("./data", image))
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.read(trainer)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 3)
        ids, conf = recognizer.predict(gray[y:y+h, x:x+w])
        print("IDS : " + str(conf))
        if conf < 50:
            c.execute("select name from users where id = (?);", (ids,))
            result = c.fetchall()
            print(result)
            if result:
                data["matches"].append({"id": ids, "name": result[0][0], "confidence": conf})
                data["status"] = "SUCCESS"
        else:
            data["status"] = "SUCCESS"
            data["message"] = "No Records Found"
    c.close()
    return jsonify(data)  # json.dumps(data, ensure_ascii=False)
