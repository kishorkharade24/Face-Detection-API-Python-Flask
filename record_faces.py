import cv2
import numpy as np
import sqlite3
import os


def create_face_records():
    if not os.path.exists('./dataset'):
        os.makedirs('./dataset')
    connection = sqlite3.connect('database.db')
    c = connection.cursor()

    return "SUCCESS"
