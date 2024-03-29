import rasterio
import rasterio.features
from fiona import collection
from shapely import geometry
import os, shutil
from math import floor
import sys, getopt
import re
import random

def main(argv):
   inputfile = ""
   try:
      opts, args = getopt.getopt(argv,"hi:o:",["cfile="])
   except getopt.GetoptError:
      print('test.py -i <inputfile>')
      sys.exit(2)
   for opt, arg in opts:
      if opt == '-h':
         print('test.py -i <inputfile>')
         sys.exit()
      elif opt in ("-i", "--ifile"):
         inputfile = arg

   print('Input file is: ', inputfile)
   print("Reading configuration...")

   with open(inputfile, 'r') as cfg:
      content = cfg.readlines()

      orig_dir = content[0][content[0].find(':') + 2 : -1]
      orig_dir_rgb = content[1][content[1].find(':') + 2 : -1]
      base_dir = content[2][content[2].find(':') + 2 : -1]
      base_dir_rgb = content[3][content[3].find(':') + 2 : -1]

      os.makedirs(base_dir)
      train_dir = os.path.join(base_dir, 'train')
      val_dir   = os.path.join(base_dir, 'validation')
      test_dir  = os.path.join(base_dir, 'test')

      os.mkdir(train_dir)
      os.mkdir(val_dir)
      os.mkdir(test_dir)

      os.makedirs(base_dir_rgb)
      train_dir_rgb = os.path.join(base_dir_rgb, 'train')
      val_dir_rgb   = os.path.join(base_dir_rgb, 'validation')
      test_dir_rgb  = os.path.join(base_dir_rgb, 'test')

      os.mkdir(train_dir_rgb)
      os.mkdir(val_dir_rgb)
      os.mkdir(test_dir_rgb)

      split_ratios = content[4][content[4].find(':') + 2 : - 1]
      split_ratios = re.split('/', split_ratios)
      split_ratios = [int(x) / 100 for x in split_ratios]

      nbr_class = content[5][content[5].find(':') + 2 : -1]
      orig_data_dirs     = {}
      train_dirs         = {}
      val_dirs           = {}
      test_dirs          = {}
      orig_data_dirs_rgb = {}
      train_dirs_rgb     = {}
      val_dirs_rgb       = {}
      test_dirs_rgb      = {}

      data_classes = content[6 : 6 + int(nbr_class)]
      data_classes = [x[0 : -1] for x in data_classes] # Removing newline
      nbr_images   = {}

      for data_class in data_classes:

         curr_orig_dir  = os.path.join(orig_dir, data_class)
         curr_train_dir = os.path.join(train_dir, data_class)
         curr_val_dir   = os.path.join(val_dir, data_class)
         curr_test_dir  = os.path.join(test_dir, data_class)

         os.mkdir(curr_train_dir)
         os.mkdir(curr_val_dir)
         os.mkdir(curr_test_dir)

         orig_data_dirs[data_class] = curr_orig_dir
         train_dirs[data_class]     = curr_train_dir
         val_dirs[data_class]       = curr_val_dir
         test_dirs[data_class]      = curr_test_dir

         curr_orig_dir_rgb  = os.path.join(orig_dir_rgb, data_class)
         curr_train_dir_rgb = os.path.join(train_dir_rgb, data_class)
         curr_val_dir_rgb   = os.path.join(val_dir_rgb, data_class)
         curr_test_dir_rgb  = os.path.join(test_dir_rgb, data_class)

         os.mkdir(curr_train_dir_rgb)
         os.mkdir(curr_val_dir_rgb)
         os.mkdir(curr_test_dir_rgb)

         orig_data_dirs_rgb[data_class] = curr_orig_dir_rgb
         train_dirs_rgb[data_class]     = curr_train_dir_rgb
         val_dirs_rgb[data_class]       = curr_val_dir_rgb
         test_dirs_rgb[data_class]      = curr_test_dir_rgb

         nbr_images[data_class] = len(os.listdir(os.path.join(orig_dir, data_class)))

      # Shuffle data
      print("Shuffling images...")
      for data_class in data_classes:

         orig_fnames = os.listdir(orig_data_dirs[data_class]) # house.0, house.1, house.2
         orig_fnames_rgb = os.listdir(orig_data_dirs_rgb[data_class])
         for fname in orig_fnames:
            src = os.path.join(orig_data_dirs[data_class], fname)
            dst = os.path.join(orig_data_dirs[data_class], 'temp_' + fname)
            os.rename(src, dst) # Nu heter filerna temp_house.0, temp_house.1, etc.

         for fname in orig_fnames_rgb:
            src = os.path.join(orig_data_dirs_rgb[data_class], fname)
            dst = os.path.join(orig_data_dirs_rgb[data_class], 'temp_' + fname)
            os.rename(src, dst) # Nu heter filerna temp_house.0, temp_house.1, etc.

         fnames = os.listdir(orig_data_dirs[data_class]) # fnames = temp_house.0, temp_house.1, etc.
         random.shuffle(fnames) # fnames = temp_house.2, temp_house.4, etc.

         i = 0
         for fname in fnames:
            src = os.path.join(orig_data_dirs[data_class], fname) # Shuffled input
            dst = os.path.join(orig_data_dirs[data_class], orig_fnames[i]) # Shuffled input set to house.0, house.1, etc. in order.
            src_rgb = os.path.join(orig_data_dirs_rgb[data_class], fname)
            dst_rgb = os.path.join(orig_data_dirs_rgb[data_class], orig_fnames_rgb[i])
            os.rename(src, dst)
            os.rename(src_rgb, dst_rgb)
            i += 1

      print("Moving images...")
      for data_class in data_classes:
         print(data_class)
         train_range = int(split_ratios[0] * nbr_images[data_class])
         val_range   = int(split_ratios[1] * nbr_images[data_class]) + train_range
         test_range  = int(split_ratios[2] * nbr_images[data_class]) + val_range

         filename = data_class[0:-1].lower()
         print("Train...")
         fnames = [filename + '.{}.tif'.format(i) for i in range(train_range)]
         for fname in fnames:
            src = os.path.join(orig_data_dirs[data_class], fname)
            dst = os.path.join(train_dirs[data_class], fname)
            shutil.copyfile(src, dst)
            src_rgb = os.path.join(orig_data_dirs_rgb[data_class], fname)
            dst_rgb = os.path.join(train_dirs_rgb[data_class], fname)
            shutil.copyfile(src_rgb, dst_rgb)

         print("Validation...")
         fnames = [filename + '.{}.tif'.format(i) for i in range(train_range, val_range)]
         for fname in fnames:
            src = os.path.join(orig_data_dirs[data_class], fname)
            dst = os.path.join(val_dirs[data_class], fname)
            shutil.copyfile(src, dst)
            src_rgb = os.path.join(orig_data_dirs_rgb[data_class], fname)
            dst_rgb = os.path.join(val_dirs_rgb[data_class], fname)
            shutil.copyfile(src_rgb, dst_rgb)

         print("Test...")
         fnames = [filename + '.{}.tif'.format(i) for i in range(val_range, test_range)]
         for fname in fnames:
            src = os.path.join(orig_data_dirs[data_class], fname)
            dst = os.path.join(test_dirs[data_class], fname)
            shutil.copyfile(src, dst)
            src_rgb = os.path.join(orig_data_dirs_rgb[data_class], fname)
            dst_rgb = os.path.join(test_dirs_rgb[data_class], fname)
            shutil.copyfile(src_rgb, dst_rgb)

if __name__ == "__main__":
   main(sys.argv[1:])
