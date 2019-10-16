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
       content = cfg.readlines()
       lines = content
       sat_path = lines[0][18:-1] # -1 skips newline
       tile_pixels = lines[1][12:-1]
       tile_path = lines[2][12:-1]
       tile_prefix = lines[3][14:-1]
       classtype = lines[4][14:-1]
       output_path = lines[5][14:-1]
       nr_of_classes = int(lines[6][9:-1])
       print("Reading shapefiles...")
       trees = []
       classnames = []
       if not os.path.isdir(output_path+"/Untaggeds"):
           os.mkdir(output_path + "/Untaggeds")
       for i in range(nr_of_classes):
           line = lines[7+i].split(',')
           classname = line[0]
           classnames.append(classname)
           shape_path = line[1][10:-1]
           if not os.path.isdir(output_path+"/"+classname):
               os.mkdir(output_path+"/"+classname)
           shp = []
           with collection(shape_path, "r") as input:
               for point in input:
                   shp.append(geometry.shape(point['geometry']))
           trees.append(STRtree(shp))
   print("Reading satellite data...")
   with rasterio.open(sat_path) as fullsat:
       sat_width = fullsat.width
       sat_height = fullsat.height
       satmask = fullsat.dataset_mask()
       for geom, val in rasterio.features.shapes(satmask, transform=fullsat.transform):
           full = geometry.shape(geom)
           coords = geom['coordinates'][0]
           west = coords[0][0]
           north = coords[0][1]
           east = coords[2][0]
           south = coords[1][1]

   width_tiles = sat_width/int(tile_pixels)
   height_tiles = sat_height/int(tile_pixels)

   width = (east-west)/width_tiles
   height = (south-north)/height_tiles
                        # för sthlm
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
           coords = [(x,y), (x,y+height), (x+width, y+height), (x+width, y), (x,y)]
           geom = {'type' : 'Polygon', 'coordinates': [coords]}
           tile = geometry.shape(geom)
           areas = []
           has_class = 0
           for k in range(nr_of_classes):
               tree = trees[k]
               res = tree.query(tile)
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
                    + classnames[index_max].lower()[:-1] + "." + str(round(width_tiles)*i + j) + ".tif")
           else:
               shutil.copyfile(tile_path + "/" + tile_prefix + "." + str(round(width_tiles)*i
                    + j) + ".tif", output_path + "/Untaggeds/untagged." +
                    str(round(width_tiles)*i + j) + ".tif")
           x += width
       y += height
       print(i)

"""
for shp in shapes[k]:
   #intersect = shp.intersection(tile)
   if not shp.disjoint(tile):# and intersect.area/shp.area > 0.5:
       # kollar nu andelen av en viss parkeringsruta är i en tile
       # borde kolla hur mycket av tilen är täckt, kanske?

       # todo: flera olika shapes kan vara i samma tile, summera?
       # Bestäm hur vi gör om flera klasser taggar samma tile.

       has_class = 1
       break
"""
if __name__ == "__main__":
   main(sys.argv[1:])
