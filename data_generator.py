import random
import os
import numpy as np
import rasterio as rio
import keras

class DataGenerator(keras.utils.Sequence):
    'Generates data for keras'
    def __init__(self, data_dir, classes, data_from=0, data_to=1, batch_size=32, n_channels=1, dim=(128, 128), shuffle=True):
        'Initialization'
        data            = os.listdir(data_dir)
        data_len        = len(data)
        self.data_dir   = data_dir
        self.data       = data[data_len * data_from : data_len * data_to]
        self.classes    = classes
        self.batch_size = batch_size
        self.n_channels = n_channels
        self.n_classes  = len(classes)
        self.dim        = dim
        self.shuffle    = shuffle
        self.on_epoch_end()

    def __len__(self):
        'Denotes the number of batches per epoch'
        return int(np.floor(len(self.data) / self.batch_size))

    def __getitem__(self, index):
        'generate one batch of data'
        images = self.data[index * self.batch_size : (index + 1) * self.batch_size]
        images, labels = self.__data_generation(images)
        return images, labels

    def on_epoch_end(self):
        'Updates indices after each epoch'
        if self.shuffle == True:
            random.shuffle(self.data)
        
    def __data_generation(self, batch_images):
        'Generates data containing batch_size examples'
        images = np.empty((self.batch_size, *self.dim, self.n_channels))
        labels = np.empty((self.batch_size), dtype=int)

        for i in range(self.batch_size):

            'Loads the bands (n_channels) from tif in to the data to be generated'
            tif_file = batch_images[i]
            image    = np.empty((self.n_channels, *self.dim))
            with rio.open(os.path.join(self.data_dir, tif_file)) as tif:
                for k in range(self.n_channels):
                    image[k] = tif.read(k+1)
                image = np.rollaxis(image, 0, 3)

            'Fixes index for one_hot encoding'
            label = ""
            for k in range(self.n_classes):
                if self.classes[k] in tif_file:
                    label = k # index for the class
                                
            images[i,] = image
            labels[i] = label # Maybe check if label is empty
        
        return images, keras.utils.to_categorical(labels, num_classes=self.n_classes)