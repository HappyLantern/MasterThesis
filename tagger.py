import rasterio
import rasterio.features
from fiona import collection
from shapely import geometry
import os
from math import floor
import sys, getopt

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
       classtype = lines[2][14:-1]
       output_path = lines[3][14:-1]
       if classtype != "binary":
           pass
           #TODO då ska vi läsa hur många klasser som finns, och hantera alla olika shapefiles osv
       else:
           line = lines[5].split(',')
           classname = line[0][6:]
           shape_path = line[1][10:-1]

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
   tagfile = open(output_path, 'w')

   width = (east-west)/width_tiles
   height = (south-north)/height_tiles
                        # x-led 18.25367104 - 17.959218298 = 0.294452742
                        # 0.00188751758 per ruta
                        # y-led 59.362344447 - 59.234034854 = 0.128309593
                        # 0.00188690578 per ruta
   x = west
   y = north
   shapes = []
   print("Reading shapefiles...")
   with collection(shape_path, "r") as input:
       for point in input:
           shp = geometry.shape(point['geometry'])
           shapes.append(shp)
   print("Tagging tiles...")

   for i in range(floor(width_tiles)):
       x = west
       for j in range(floor(height_tiles)):

           has_parking_lot = 0
           coords = [(x,y), (x,y+height), (x+width, y+height), (x+width, y), (x,y)]
           geom = {'type' : 'Polygon', 'coordinates': [coords]}
           tile = geometry.shape(geom)

           for shp in shapes:
               if not shp.disjoint(tile):
                   has_parking_lot = 1
                   # print(i*156+j, i, j )
                   tagfile.write(str(i*floor(width_tiles)+j) + " " + str(has_parking_lot) + "\n")
                   break

               #print(geometry.shape(point['geometry']), point['properties']
           tagfile.write(str(i*floor(width_tiles)+j) + " " + str(has_parking_lot) + "\n")
           x += width
       y += height


if __name__ == "__main__":
   inputfile = main(sys.argv[1:])
