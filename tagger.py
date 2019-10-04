import rasterio
import rasterio.features
import rasterio.warp
from fiona import collection
from shapely import geometry
from matplotlib import pyplot
import os


tagfile = open("parktags.txt", 'w')
"""
with rasterio.open("satellite images/sthlmgreynew.tif") as fullsat: # fördelad på 33469,27868
    satmask = fullsat.dataset_mask()
    for geom, val in rasterio.features.shapes(satmask, transform=fullsat.transform):
        print(geom)
        full = geometry.shape(geom)
"""

start_x = 17.959218298
start_y = 59.362344447
width = 0.00188751758
height = -0.00188690578
x = start_x
y = start_y
shapes = []
with collection("shapefiles etc/sthlmpoly.shp", "r") as input:
    for point in input:
        shp = geometry.shape(point['geometry'])
        shapes.append(shp)
for i in range(68):
    x = start_x
                         # x-led 18.25367104 - 17.959218298 = 0.294452742
                         # 0.00188751758 per ruta
    for j in range(156): # y-led 59.362344447 - 59.234034854 = 0.128309593
                         # 0.00188690578 per ruta
        coords = [(x,y), (x,y+height), (x+width, y+height), (x+width, y), (x,y)]
        geom = {'type' : 'Polygon', 'coordinates': [coords]}
        tile = geometry.shape(geom)
        for shp in shapes:
            if not rasterio.coords.disjoint_bounds(tile.bounds, shp.bounds):
                has_parking_lot = 1
                print(i*156+j, i, j )
                break
            #print(geometry.shape(point['geometry']), point['properties']
        tagfile.write(i*156+j, has_parking_lot)
        x += width
    y += height

"""
for filename in os.listdir("qgistiles"):
    has_parking_lot = 0
    if filename.endswith(".tif"):

        with rasterio.open("qgistiles/"+filename) as tile:
            mask = tile.dataset_mask()

            for geom, val in rasterio.features.shapes(mask, transform=tile.transform):
                # geom = rasterio.warp.transform_geom("EPSG:4326", "EPSG:32634", geom, precision=9)

                tileshape = geometry.shape(geom)
                print(geom)
"""

tagfile.close()
