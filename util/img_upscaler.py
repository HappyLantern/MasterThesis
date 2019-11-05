import numpy as np
import rasterio as rio
import matplotlib.pyplot as plt

file = 'C:\\Users\\Kevinski\\Programming\\MasterThesis\\Data\\Images\\Sthlm\\tiles256gray\\tiles256gray.0.tif'

with rio.open(file) as file:
    band = np.random.rand(32, 32)
    print(band)

    upscale_factor = 4
    new_band = np.zeros([band.shape[0] * upscale_factor, band.shape[1] * upscale_factor])
    band_x = 0
    band_y = 0
    new_band_x = 0
    new_band_y = 0

    print(band.shape)
    print(new_band.shape)
    for i in range(band.shape[0] * band.shape[0]):
        print(band_x, band_y)
        print(new_band_x, new_band_y)
        print(band[band_x][band_y])

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
        
    print(new_band)
    
    f = plt.figure(1)
    plt.imshow(band)
    g = plt.figure(2)
    plt.imshow(new_band)
    plt.show()
    


