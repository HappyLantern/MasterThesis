import numpy as np
import os
import rasterio
import numpy as np
base_dir = '../Data/test_for_generator_rgb_wash'

for dir in os.listdir(base_dir):
    print("Rescaling "+dir+" folder...")
    curr_dir = os.path.join(base_dir, dir)

    for folder in os.listdir(curr_dir):
        print("at", folder)
        curr_folder = os.path.join(curr_dir, folder)


        for filename in os.listdir(curr_folder):
            if filename.endswith(".tif"):
                curr_file = os.path.join(curr_folder, filename)
                bands = []
                with rasterio.open(curr_file) as f:
                    profile = f.profile

                    for i in range(f.count):
                        bands.append(f.read(i+1))
                        bands[i] = bands[i]/8
                        bands[i] = np.rint(bands[i])
                        bands[i] = bands[i].astype('uint8')

                    profile.update(dtype=rasterio.uint8, nodata=255.0)
                with rasterio.open(curr_file, 'w', **profile) as g:
                    for i in range(len(bands)):
                        g.write(bands[i], i+1)
