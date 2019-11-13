import csv
import json
from fiona import collection
from shapely import geometry

def addPoly(polyout, coords):
    for p in coords:
        point = geometry.Point(float(p[0]), float(p[1]))
        points.append((float(p[0]), float(p[1])))
    poly = geometry.Polygon(points)
    polyout.write({
        'properties': {
            'name': a
        },
        'geometry'  : geometry.mapping(poly)
    })


with open('C:/Users/A552079/Documents/MasterThesis/Data/jsondata/forest.geojson', encoding="utf-8") as f:
    data =  json.load(f)
coords = data['features'][0]['geometry']['coordinates']

polySchema = { 'geometry': 'Polygon', 'properties': { 'name': 'str' } }
pointSchema = { 'geometry': 'Point', 'properties': { 'name': 'str' } }
multiPolySchema = { 'geometry': 'MultiPolygon', 'properties': { 'name': 'str' } }
with collection(
    "Data/shapefiles/forestpoly.shp", "w", "ESRI Shapefile", polySchema) as polyout:
        a=0
        for feature in data['features']:
            points = []
            a+=1
            geo = feature['geometry']
            if(geo['type'] == 'Polygon'):
                addPoly(polyout, geo['coordinates'][0])
            if(geo['type'] == 'MultiPolygon'):
                for coords in geo['coordinates']: # kan vara fel? ibland finns inre former som inte ska tillhöra multin
                    addPoly(polyout, coords[0])
            """
            if(geo['type'] == 'Point'):
                pass
                p = geo['coordinates']
                point = geometry.Point(float(p[0]), float(p[1]))
                pointout.write({
                    'properties': {
                        'name': a
                    },
                    'geometry'  : geometry.mapping(point)
            })
            """

"""
with collection("sthlmhuspoly.shp", "r") as input:
    for point in input:
        print(geometry.shape(point['geometry']), point['properties'])
with collection("sthlmhuspoint.shp", "r") as input:
    for point in input:
        print(geometry.shape(point['geometry']), point['properties'])
"""
