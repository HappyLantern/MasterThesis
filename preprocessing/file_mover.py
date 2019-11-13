import numpy as np
import rasterio as rio
import matplotlib.pyplot as plt
import os, shutil

city = "wash"
final_dst = "../Data/final data"
base_dir = '../Data/scaled data/test_for_generator_'+city+'_scaled'
for dir in os.listdir(base_dir):
    print("\nMoving "+dir+" folder...")
    curr_dir = os.path.join(base_dir, dir)

    for folder in os.listdir(curr_dir):
        print("at", folder)
        curr_folder = os.path.join(curr_dir, folder)
        
        for f in os.listdir(curr_folder):
            src = os.path.join(curr_folder, f)
            fnf = city + "." + f
            dst = os.path.join(final_dst, fnf)
            shutil.copyfile(src,dst)