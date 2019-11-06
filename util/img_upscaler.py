import numpy as np
import rasterio as rio
import matplotlib.pyplot as plt
import os

base_dir = '../Data/test_for_generator_rgb_wash'

for dir in os.listdir(base_dir):
    print("Upscaling "+dir+" folder...")
    curr_dir = os.path.join(base_dir, dir)

    for folder in os.listdir(curr_dir):
        print("at", folder)
        curr_folder = os.path.join(curr_dir, folder)

        for f in os.listdir(curr_folder):
            with rio.open(os.path.join(curr_folder,f)) as file:
                profile = file.profile
                bands = []
                upscale_factor = 4
                for o in range(file.count):
                    band = file.read(o+1)
                    new_band = np.zeros([band.shape[0] * upscale_factor, band.shape[1] * upscale_factor], dtype='uint8')
                    band_x = 0
                    band_y = 0
                    new_band_x = 0
                    new_band_y = 0

                    #print(band.shape)
                    #print(new_band.shape)
                    for i in range(band.shape[0] * band.shape[0]):
                        #print(band_x, band_y)
                        #print(new_band_x, new_band_y)
                        #print(band[band_x][band_y])

                        for k in range(upscale_factor):
                            new_band[new_band_x][new_band_y + k]     = band[band_x, band_y]
                            new_band[new_band_x + k][new_band_y]     = band[band_x, band_y]
                            new_band[new_band_x + k][new_band_y + k] = band[band_x, band_y]
                            new_band[new_band_x + k][new_band_y + 1] = band[band_x, band_y]
                            new_band[new_band_x + 1][new_band_y + k] = band[band_x, band_y]
                            new_band[new_band_x + 2][new_band_y + k] = band[band_x, band_y]
                            new_band[new_band_x + k][new_band_y + 2] = band[band_x, band_y]

                        band_x = band_x + 1
                        if (band_x % band.shape[0] == 0):
                            band_x = 0
                            band_y = band_y + 1

                        new_band_x = new_band_x + upscale_factor
                        if (new_band_x % new_band.shape[0] == 0):
                            new_band_x = 0
                            new_band_y = new_band_y + upscale_factor

                    bands.append(new_band)

            with rio.open(os.path.join(path,f), 'w', **profile) as g:
                for i in range(len(bands)):
                    #print(bands[i].shape[0], f)
                    g.write(bands[i], i+1)

"""
print(new_band)

f = plt.figure(1)
plt.imshow(band)
g = plt.figure(2)
plt.imshow(new_band)
plt.show()
"""
