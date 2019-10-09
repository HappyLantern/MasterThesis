from keras import layers
from keras import models
from keras.utils import to_categorical

import numpy as np

images = np.load('images.npy')
labels = np.load('labels.npy')

images = images.reshape((10385, 256, 256, 1))
images = images.astype('float32') / 65536
print(labels[0])
print(labels[0])
print(images.shape)
print(labels.shape)

model = models.Sequential()
model.add(layers.Conv2D(32, (3, 3), activation='relu', input_shape=(256, 256, 1)))
model.add(layers.MaxPooling2D((2, 2)))
model.add(layers.Conv2D(64, (3, 3), activation='relu'))
model.add(layers.MaxPooling2D((2, 2)))
model.add(layers.Conv2D(128, (3, 3), activation='relu'))
model.add(layers.Flatten())
model.add(layers.Dense(128, activation='relu'))
model.add(layers.Dense(1, activation='sigmoid'))

model.compile(optimizer='rmsprop', 
              loss='binary_crossentropy', 
              metrics=['precision', 'F1'])

model.fit(images, labels, epochs=5, batch_size=32)
