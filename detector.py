import cv2
import numpy as np
import sqlite3
import os
import json
from flask import jsonify

# Constant
trainer = "recognizer/trainingData.yml"


def detect_faces(image):
    try:
        data = {}
        data["matches"] = []
        data["message"] = "No Records Found"
        connection = sqlite3.connect('database.db')
        c = connection.cursor()
        if not os.path.isfile(trainer):
            return jsonify({"message": "Please execute trainer first.", "status": "FAILURE"})
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
            print("IDS : " + str(ids) + " : Conf : " + str(conf))
            if conf < 55:
                c.execute("select name, emp_id from users where id = (?);", (ids,))
                result = c.fetchall()
                print(result)
                if result:
                    data["matches"].append({"id": ids, "name": result[0][0], "emp_id": result[0][1], "confidence": conf})
                    data["status"] = "SUCCESS"
            else:
                data["status"] = "SUCCESS"
                data["message"] = "No Records Found"
        c.close()
    except Exception as e:
        print("Exception : ", e)
        return jsonify({"message": "Error while getting faces", "status": "FAILURE"})

    return jsonify(data)
