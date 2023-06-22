import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt
import panda as pd
from PIL import Image

img = Image("")



#PROVA A CASA CON UN COMPUTER PIU POTENTE
'''
#fashion_mnist = tf.keras.datasets.fashion_mnist

(train_images, train_labels), (test_images, test_labels) = fashion_mnist.load_data()


class_names = ['T-shirt/top', 'Trouser', 'Pullover', 'Dress', 'Coat',
               'Sandal', 'Shirt', 'Sneaker', 'Bag', 'Ankle boot']

print(tf.__version__)
'''
'''
losses = ["mean_squared_error", 'mean_absolute_error', 'mean_absolute_percentage_error', 'mean_squared_logarithmic_error', ]

for name in losses:
    model = tf.keras.Sequential([tf.keras.layers.Dense(units = 1, input_shape=[1])])
    model.compile(optimizer="sgd", loss = name)

    xs = np.arange(-5, 11)
    ys = xs*xs

    model.fit(xs, ys, epochs = 1000, verbose = 0)

    sum = 0
    values = [12, 5, 1492, -92]
    for i in values:
        sum += abs(model.predict([i])-(i*i))
    print(name)
    print(sum/len(values))

'''




