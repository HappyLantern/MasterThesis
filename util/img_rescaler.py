import numpy as np
import os
import rasterio
base_dir = '../Data/test_for_generator'

train_dir = os.path.join(base_dir, 'train')
test_dir = os.path.join(base_dir, 'test')
validation_dir = os.path.join(base_dir, 'validation')
"""
print("rescaling training data...")
for folder in os.listdir(train_dir):
    print("at", folder)
    if folder == "Parkings":
        for filename in os.listdir(train_dir+"/"+folder):
            with rasterio.open(train_dir+"/"+folder+"/"+filename) as f:
                profile = f.profile
                #print(profile)
                profile.update(nodata=255.0, dtype=rasterio.uint8)
                #print(profile)
                a = f.read(1)
                a = a/8 # maxvalue is ~2000, should be 255
                a = a.astype('uint8')
            with rasterio.open(train_dir+"/"+folder+"/"+filename, 'w', **profile) as g:
                g.write(a, 1)
"""
print("rescaling test data...")
for folder in os.listdir(test_dir):
    print("at", folder)
    for filename in os.listdir(test_dir+"/"+folder):
        with rasterio.open(test_dir+"/"+folder+"/"+filename) as f:
            profile = f.profile
            profile.update(dtype=rasterio.uint8, nodata=255.0)
            a = f.read(1)
            a = a/8
            a = a.astype('uint8')
        with rasterio.open(test_dir+"/"+folder+"/"+filename, 'w', **profile) as g:
            g.write(a, 1)
"""
print("rescaling validation data...")
for folder in os.listdir(validation_dir):
    print("at", folder)
    for filename in os.listdir(validation_dir+"/"+folder):
        with rasterio.open(validation_dir+"/"+folder+"/"+filename) as f:
            profile = f.profile
            profile.update(dtype=rasterio.uint16)
            a = f.read(1)
            a = a/8
            a = a.astype('uint16')
        with rasterio.open(validation_dir+"/"+folder+"/"+filename, 'w', **profile) as g:
            g.write(a, 1)
"""
