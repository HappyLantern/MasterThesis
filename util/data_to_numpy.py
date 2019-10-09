import rasterio as rio
import os
import numpy as np

path = "./Sthlm/tiles256gray/"

""" train_images = []

for filename in os.listdir(path):
    with rio.open(path + filename) as src:

        if src.height == 256 and src.width == 256:
            img = src.read(1) # dtype = uint16 0-65536
            train_images.append(img)
            #train_images[i, :, :] = img

train_images = np.array(train_images)
np.save('train_images', train_images)
print(train_images.shape) """
train_images = np.load('train_images.npy')
print(train_images.shape)
print(train_images[0])

path2 = "./parktags.txt"

train_labels = []
labels = open(path2, "r")
for label in labels:
    train_labels.append(int(label))

train_labels = np.array(train_labels)
np.save('train_labels', train_labels)

train_labels = np.load('train_labels.npy')
print(train_labels.shape)








