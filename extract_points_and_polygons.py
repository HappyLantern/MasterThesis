import csv
import json
from fiona import collection
from shapely import geometry

with open('sthlm.geojson', encoding="utf-8") as f:
    data =  json.load(f)
coords = data['features'][0]['geometry']['coordinates']

polySchema = { 'geometry': 'Polygon', 'properties': { 'name': 'str' } }
pointSchema = { 'geometry': 'Point', 'properties': { 'name': 'str' } }
with collection(
    "sthlmpoly.shp", "w", "ESRI Shapefile", polySchema) as polyout:
        with collection(
            "sthlmpoint.shp", "w", "ESRI Shapefile", pointSchema) as pointout:
            a=0
            for feature in data['features']:
                points = []
                a+=1
                geo = feature['geometry']
                if(geo['type'] == 'Polygon'):
                    for p in geo['coordinates'][0]:
                        point = geometry.Point(float(p[0]), float(p[1]))
                        points.append((float(p[0]), float(p[1])))
                    poly = geometry.Polygon(points)
                    polyout.write({
                        'properties': {
                            'name': a
                        },
                        'geometry'  : geometry.mapping(poly)
                })
                if(geo['type'] == 'MultiPolygon'):
                    print("todo MultiPolygon")
                if(geo['type'] == 'Point'):
                    p = geo['coordinates']
                    point = geometry.Point(float(p[0]), float(p[1]))
                    pointout.write({
                        'properties': {
                            'name': a
                        },
                        'geometry'  : geometry.mapping(point)
                })


with collection("sthlmpoly.shp", "r") as input:
    for point in input:
        print(geometry.shape(point['geometry']), point['properties'])
with collection("sthlmpoint.shp", "r") as input:
    for point in input:
        print(geometry.shape(point['geometry']), point['properties'])
