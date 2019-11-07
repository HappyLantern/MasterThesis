import numpy as np
import rasterio as rio
import matplotlib.pyplot as plt
import os

base_dir = '../Data/scaled data/test_for_generator_rgb_rio_scaled'
gray_dir = '../Data/scaled data/test_for_generator_rio_scaled'

for dir in os.listdir(base_dir):
    print("\nUpscaling "+dir+" folder...")
    curr_dir = os.path.join(base_dir, dir)

    for folder in os.listdir(curr_dir):
        print("at", folder)
        curr_folder = os.path.join(curr_dir, folder)
        
        for f in os.listdir(curr_folder):
            with rio.open(os.path.join(curr_folder,f)) as file:

                profile = file.profile
            
                bands = []
                upscale_factor = 4
                for o in range(4): # file.count? But it has to be 4 for the model. wash has 8. 
                    band = file.read(o+1)
                    # 32 is the band.shape[0] or 1, but hardcoded because we have not cleaned out edges with weird shapes
                    # Right now, the edges get enlarged to 32,32 with 0 in the new values.
                    new_band = np.zeros([32 * upscale_factor, 32 * upscale_factor], dtype='uint8')
                    band_x = 0
                    band_y = 0
                    new_band_x = 0
                    new_band_y = 0
                
                    
                    for i in range(band.shape[0] * band.shape[1]):

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

            with rio.open(os.path.join(gray_dir, dir, folder, f), 'w', driver ='GTiff',
                            width=128, height=128, dtype='uint8', count=len(bands)+1) as g:

                for i in range(len(bands)):
                    g.write(bands[i], i+2)
