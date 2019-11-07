import rasterio
import rasterio.features
from fiona import collection
from shapely import geometry
from shapely.strtree import STRtree
import os
from math import floor
import sys, getopt
import shutil

def main(argv):
   inputfile = "config.txt"
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
       lines           = cfg.readlines()
       sat_path        = lines[0][18:-1] # -1 skips newline
       tile_pixels     = lines[1][12:-1]
       tile_path       = lines[2][12:-1]
       tile_prefix     = lines[3][14:-1]
       tile_path_rgb   = lines[4][16:-1]
       tile_prefix_rgb = lines[5][19:-1]
       output_path     = lines[6][14:-1]
       output_rgb      = lines[7][13:-1]
       nr_of_classes   = int(lines[8][9:-1])

       print("Reading shapefiles...")
       trees         = []
       classnames    = []
       class_indices = []

       if not os.path.isdir(output_path):
           os.mkdir(output_path)

       if not os.path.isdir(output_rgb):
           os.mkdir(output_rgb)

       if not os.path.isdir(output_path+"/Untaggeds"):
           os.mkdir(output_path + "/Untaggeds")

       if not os.path.isdir(output_rgb+"/Untaggeds"):
           os.mkdir(output_rgb + "/Untaggeds")

       for i in range(nr_of_classes):
           line       = lines[9+i].split(',')
           classname  = line[0]
           shape_path = line[1][10:-1]
           class_indices.append(0)
           classnames.append(classname)

           if not os.path.isdir(output_path+"/"+classname):
               os.mkdir(output_path+"/"+classname)

           if not os.path.isdir(output_rgb+"/"+classname):
               os.mkdir(output_rgb+"/"+classname)

           shp = []
           with collection(shape_path, "r") as input:
               for point in input:
                   shp.append(geometry.shape(point['geometry']))
           trees.append(STRtree(shp))
   class_indices.append(0)

   print("Reading satellite data...")
   with rasterio.open(sat_path) as fullsat:
       sat_width  = fullsat.width
       sat_height = fullsat.height
       satmask    = fullsat.dataset_mask()

       for geom, val in rasterio.features.shapes(satmask, transform=fullsat.transform):
           full   = geometry.shape(geom)
           coords = geom['coordinates'][0]
           west   = coords[0][0]
           north  = coords[0][1]
           east   = coords[2][0]
           south  = coords[1][1]

   if sat_path == "../satellite images/washgreynew.tif":
       west  = -77.114237367
       south = 38.880489803
       east  = -76.999183819
       north = 38.97260028
   width_tiles  = sat_width/int(tile_pixels)
   height_tiles = sat_height/int(tile_pixels)
   width        = (east-west)/width_tiles
   height       = (south-north)/height_tiles
                        # för sthlmrgb
                        # x-led 18.25367104 - 17.959218298 = 0.294452742
                        # 0.00188751758 per ruta
                        # y-led 59.362344447 - 59.234034854 = 0.128309593
                        # 0.00188690578 per ruta
  
   x = west
   y = north

   print("Tagging tiles...")
   for i in range(floor(height_tiles)):
       x = west

       for j in range(floor(width_tiles)):
           has_class = 0
           coords    = [(x,y), (x,y+height), (x+width, y+height), (x+width, y), (x,y)]
           geom      = {'type' : 'Polygon', 'coordinates': [coords]}
           tile      = geometry.shape(geom)
           areas     = []

           for k in range(nr_of_classes):
               tree = trees[k]
               res  = tree.query(tile)
               area = 0

               for s in res:
                   has_class = 1

                   try:
                       area += s.intersection(tile).area
                       # hanterar inte om flera shapes överlappar, det är dock doable
                   except Exception as e:
                       s = s.buffer(0)
                       area += s.intersection(tile).area
               areas.append(area)

           if has_class == 1:
               index_max = max(range(len(areas)), key=areas.__getitem__)

               shutil.copyfile(tile_path + "/" + tile_prefix + "." + str(round(width_tiles)*i
                    + j) + ".tif", output_path + "/" + classnames[index_max] + "/"
                    + classnames[index_max].lower()[:-1] + "." + str(class_indices[index_max]) + ".tif")

               shutil.copyfile(tile_path_rgb + "/" + tile_prefix_rgb + "." + str(round(width_tiles)*i
                    + j) + ".tif", output_rgb + "/" + classnames[index_max] + "/"
                    + classnames[index_max].lower()[:-1] + "." + str(class_indices[index_max]) + ".tif")

               class_indices[index_max]+=1

           else:
               shutil.copyfile(tile_path + "/" + tile_prefix + "." + str(round(width_tiles)*i
                    + j) + ".tif", output_path + "/Untaggeds/untagged." +
                    str(class_indices[nr_of_classes]) + ".tif")

               shutil.copyfile(tile_path_rgb + "/" + tile_prefix_rgb + "." + str(round(width_tiles)*i
                    + j) + ".tif", output_rgb + "/Untaggeds/untagged." +
                    str(class_indices[nr_of_classes]) + ".tif")

               class_indices[nr_of_classes]+=1
           x += width
       y += height

if __name__ == "__main__":
   main(sys.argv[1:])
