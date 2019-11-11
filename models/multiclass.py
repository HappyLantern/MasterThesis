from keras import layers
from keras import models
from keras import optimizers
from ourVGG16 import ourVGG16
from keras.preprocessing.image import ImageDataGenerator
import numpy as np
import os, shutil
import rasterio
from data_generator import DataGenerator



base_dir = '../Data/vgg_data'
classes = ['commercial', 'industrial', 'residential', 'parque', 'parking', 'forest']
model = ourVGG16(len(classes), input_shape=(256, 256, 5))

model.compile(optimizer=optimizers.RMSprop(lr=1e-5),
              loss='categorical_crossentropy',
              metrics=['acc'])

train_datagen = DataGenerator(base_dir, classes, n_channels=5, dim=(256,256))

history = model.fit_generator(
      train_datagen,
      epochs=30)
"""
model.save('multiclass.h5')

import matplotlib.pyplot as plt

acc = history.history['acc']
val_acc = history.history['val_acc']
loss = history.history['loss']
val_loss = history.history['val_loss']

epochs = range(len(acc))

plt.plot(epochs, acc, 'bo', label='Training acc')
plt.plot(epochs, val_acc, 'b', label='Validation acc')
plt.title('Training and validation accuracy')
plt.legend()

plt.figure()

plt.plot(epochs, loss, 'bo', label='Training loss')
plt.plot(epochs, val_loss, 'b', label='Validation loss')
plt.title('Training and validation loss')
plt.legend()

plt.show()
"""