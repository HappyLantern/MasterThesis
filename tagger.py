import rasterio
import rasterio.features
from fiona import collection
from shapely import geometry
import os


with rasterio.open("satellite images/sthlmgreynew.tif") as fullsat:
    sat_width = fullsat.width
    sat_height = fullsat.height
    satmask = fullsat.dataset_mask()
    for geom, val in rasterio.features.shapes(satmask, transform=fullsat.transform):
        print(geom)
        full = geometry.shape(geom)
        coords = geom['coordinates'][0]
        west = coords[0][0]
        north = coords[0][1]
        east = coords[2][0]
        south = coords[1][1]

tile_pixels = 256
width_tiles = sat_width/tile_pixels
height_tiles = sat_height/tile_pixels
tagfile = open("parktags.txt", 'w')

width = (east-west)/width_tiles
height = (south-north)/height_tiles
x = west
y = north
print(width, height)
shapes = []
with collection("shapefiles etc/sthlmpoly.shp", "r") as input:
    for point in input:
        shp = geometry.shape(point['geometry'])
        shapes.append(shp)
for i in range(68):
    x = west
                         # x-led 18.25367104 - 17.959218298 = 0.294452742
                         # 0.00188751758 per ruta
    for j in range(156): # y-led 59.362344447 - 59.234034854 = 0.128309593
                         # 0.00188690578 per ruta
        has_parking_lot = 0
        coords = [(x,y), (x,y+height), (x+width, y+height), (x+width, y), (x,y)]
        geom = {'type' : 'Polygon', 'coordinates': [coords]}
        tile = geometry.shape(geom)

        for shp in shapes:
            if not shp.disjoint(tile):
                has_parking_lot = 1
                # print(i*156+j, i, j )
                tagfile.write(str(i*156+j) + " " + str(has_parking_lot) + "\n")
                break

            #print(geometry.shape(point['geometry']), point['properties']
        tagfile.write(str(i*156+j) + " " + str(has_parking_lot) + "\n")

        x += width
    y += height
    if i == 0:
        pass
tagfile.close()
