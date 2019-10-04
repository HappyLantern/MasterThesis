import rasterio
import rasterio.features
import rasterio.warp
from fiona import collection
from shapely import geometry
from matplotlib import pyplot
import os

for filename in os.listdir("qgistiles"):
    if filename.endswith(".tif"):
        with rasterio.open("qgistiles/"+filename) as tile: #  'w', driver="GTiff"
            #array = tile.read(1)
            mask = tile.dataset_mask()
            #tile.update_tags('coordinates', [[(a,b)]])
            #print(array.shape)
            #pyplot.imshow(array,cmap='gray')
            #pyplot.show()

            for geom, val in rasterio.features.shapes(mask, transform=tile.transform):
                """
                print(geom)
                glist = []
                for coords in geom['coordinates'][0]:
                    glist.append(coords)
                    #tile.update_tags('coordinates', [[(a,b)]])
                geom['coordinates'][0] = glist
                print(geom)
                """
                geom = rasterio.warp.transform_geom("EPSG:4326", "EPSG:32634", geom, precision=9)

                tileshape = geometry.shape(geom)

            with collection("shapefiles etc/sthlmpoly.shp", "r") as input: # OBS hårdkodat för sthlmgrey
                for point in input:
                    """  90, 212 + 14848, 7168

                    334478.176846732, 6580192.332091706 ger  334478-326525 = 7950 i x-led, på 90+14848 = 14938
                    och 6583620 - 6580192 = 3428 i y-led på 7380, ger 1.87899371, 2.15285881

                    Betyder att givet en koordinat, t ex 335905, 6580682
                    kan vi subtrahera bort basen (326525.859) till 9380, och multiplicera med 1.879 till 17625 för x
                    för y, ta också bort basen, till 2938, och multiplicera med 2.153 till 6325.5

                    17625, 6325.5



                    """
                    #print(point)
                    p = rasterio.warp.transform_geom("EPSG:4326", "EPSG:32634", point['geometry'], precision=9)

                    """
                    enl mätverktyg 14250 till 16770 ger 1.95564912 och 1.995

                    #print(p)
                    for coords in p['coordinates'][0]: # 326525.8594834,6570069.2548295 är start
                        coords[0] -= 326800.8594834    # 343906.6801505,6583620.1083060 är slut
                        coords[1] -= 6583950.1083060   # ger 17380.8207 i x-led, 13550.8535 i y-led fördelat på 33469,27868
                        coords[0] *= 1.8789937        # dvs multiplicerar vi t ex resten i x-led med 33469/17380.8 = 1.92563
                        coords[1] *= -2.15285881        # och i y-led blir det 27868/13550.8535 = 2.05655
                    #print(coords)
                    """
                    shp = geometry.shape(p)
                    if not rasterio.coords.disjoint_bounds(shp.bounds, tileshape.bounds):
                        #print("\""+tile.name[18:-4] + "\" ", end='')
                        print(tile.name)

                    #print(geometry.shape(point['geometry']), point['properties']



"""
with rasterio.open("satellite images/sthlmgrey.tif") as tile:
    mask = tile.dataset_mask()
    print(tile)
    for geom, val in rasterio.features.shapes(mask, transform=tile.transform):
        print(geom)

        full = geometry.shape(geom)

"""
