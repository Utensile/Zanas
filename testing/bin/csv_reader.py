import pandas as pd
import cv2
import matplotlib.pyplot as plt
import numpy as np
from sklearn.model_selection import train_test_split

dataset_path = 'C:/Users/simon/Desktop/testing/rocket.csv'
image_size = (48, 48, 3)  # Aggiunto 3 per immagini RGB

def load():
    data = pd.read_csv(dataset_path)
    pixels = data['pixels'].tolist()
    width, height, depth = 48, 48, 3  # Aggiunto depth per immagini RGB
    faces = []
    for pixel_sequence in pixels:
        
        pixel_sequence = pixel_sequence[:-1]
        if pixel_sequence :
            face = [int(pixel) for pixel in pixel_sequence.split(' ')]
            face = np.asarray(face).reshape(width, height, depth)  # Aggiunto depth per immagini RGB
            a = face
            face = cv2.resize(face.astype('uint8'), image_size)
            faces.append(face.astype('float32'))
    faces = np.asarray(faces)
    A = faces
    faces = np.expand_dims(faces, -1)
    return faces, A

faces, A = load()
plt.imshow(A[0].astype("uint8"))


