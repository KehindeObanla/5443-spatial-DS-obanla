import sys
import os
from rtree import index
from flask import Flask
from flask import request
from flask import jsonify
from json import loads
from flask_cors import CORS
from misc_functions import *
import glob
import json
import math
from rtree import index
import random
import networkx as nx
import matplotlib.pyplot as plt
from networkx.utils import open_file
from decimal import Decimal
from networkx.algorithms import tree
from shapely.geometry import LineString
from shapely.geometry import Point

idx = index.Index()
idx2 = index.Index()
pathRoad ='assignments\\A04\\assets\\json\\Primary_Roads.geojson\\Primary_Roads.geojson'



def finddistance():
    """ Description: return a distance between two points
        Params:
            None
        Example: http://localhost:8080/distance/?lnglat=
    """
    lng, lat, lng1, lat1 = -124.000, 34.000, -124.0020, 34.0020
    lnglat = (float(lng), float(lat))
    lnglat1 = (float(lng1), float(lat1))
    return haversine(lnglat, lnglat1, miles=True)


def load_data(path):
    """ Given a path, load the file and handle it based on its
        extension type. So far I have code for json and csv files.
    """
    _, ftype = os.path.splitext(path)   # get fname (_), and extenstion (ftype)

    if os.path.isfile(path):            # is it a real file?
        with open(path, 'r', encoding='utf-8') as f:

            if ftype == ".json" or ftype == ".geojson":  # handle json
                data = f.read()
                print(type(data))
                if isJson(data):
                    print(type(data))
                    return json.loads(data)

            elif ftype == ".csv":       # handle csv with csv reader
                with open(path, newline='') as csvfile:
                    data = csv.DictReader(csvfile)


def isJson(data):
    """ Helper method to test if val can be json
        without throwing an actual error.
    """
    try:
        json.loads(data)
        return True
    except ValueError:
        return False

def buildLineStringRtree(path):
    uniqueueRoadid = {}
    count =0
    data = load_data(path)
    feature = data['features']
    print(len(feature))
    for row in feature:
        resultlist= row["geometry"]["coordinates"]
        uniqueueRoadid[count] = row
        coords = LineString(resultlist[0])
        left,right,bottom, top = coords.bounds
        idx2.insert(count, (left,right,bottom, top))
        count+=1
    print(len(uniqueueRoadid))
    print(count)
    return idx2, uniqueueRoadid


""" CITIES = load_data(
    "assignments\\A04\\assets\\json\\countries_states\\major_cities.geojson")
STATES = load_data(
    "assignments\\A04\\assets\\json\\countries_states\\states.json") """
NE_10m_roads ="assignments\\A04\\assets\\json\\ne_10m_roads_north_america\\newroad.shp"
NE_10m_roadsGeo ="assignments\\A04\\assets\\json\\ne_10m_roads_north_america\\newroadgeo.geojson"
populatedPlacespath = "assignments\\A04\\assets\\json\\ne_10m_populated_places\\populatedplacesgeo.geojson"
createdGraph ="assignments\\A04\\assets\\output"
primaryroads = "assignments\\A04\\assets\\json\\shapefile\\primaryroadshap.shp"
primaryroadsGeojson ="assignments\\A04\\assets\\json\Primary_Roads.geojson\\Primary_Roads.geojson"
""" shape file to graph """
shapefileToGraph = nx.read_shp(NE_10m_roads,simplify=True,geom_attrs=True,strict=False)
G2 = shapefileToGraph.to_undirected()
path2 ="assignments\\A04\\assets\\json\\mst"
idx2,rtreeroadid =buildLineStringRtree(NE_10m_roadsGeo)

def handle_response(data, params=None, error=None):
    """ handle_response
    """
    success = True
    if data:
        if not isinstance(data, list):
            data = [data]
        count = len(data)
    else:
        count = 0
        error = "Data variable is empty!"

    result = {"success": success, "count": count,
              "results": data, "params": params}

    if error:
        success = False
        result['error'] = error

    return (jsonify(result))

  
def validateJSON(jsonData):
    try:
        json.loads(jsonData)
    except ValueError as err:
        return False
    return True
def point_to_bbox(lng, lat, offset=.001):
    #(left, bottom, right, top)

    return (float(lng-offset), float(lat-offset), float(lng+offset), float(lat+offset))
def build_index():
    #(left, bottom, right, top)

    eqks = glob.glob(
        "assignments\\A04\\Assets\\json\\earthquake_data\\earthquakes\\*.json")
    del eqks[350:840]
    count = 0
    bad = 0
    earthquakeUniqueid = {}

    for efile in eqks:
        minlat = 999
        minlng = 999
        maxlat = -999
        maxlng = -999
        with open(efile, 'r', encoding='utf-8') as f:
            data = f.readlines()

        for row in data[2:]:
            row = row.strip()
            row = row.strip(",")
            if validateJSON(row):
                row = json.loads(row)
                lng, lat, _ = row["geometry"]["coordinates"]
                earthquakeUniqueid[count] = row
                if lng < minlng:
                    minlng = lng
                if lat < minlat:
                    minlat = lat
                if lng > maxlng:
                    maxlng = lng
                if lat > maxlat:
                    maxlat = lat

                left, bottom, right, top = point_to_bbox(lng, lat)
                idx.insert(count, (left, bottom, right, top))
                count += 1
            else:
                bad += 1
        """  print(count) """
    return idx, earthquakeUniqueid
def nearestNeighbors(lng, lat):
    answer_Collection = {
        "type": "FeatureCollection",
        "features": []
    }
    answer_CollectionpolyGon = {
        "type": "FeatureCollection",
        "features": [
            {

            'type': 'Feature',
            'geometry': {
                'type': 'Polygon',
                'coordinates':[]
            }
            }
          
       ]
    }

    idx, rtreeid = build_index()
    left, bottom, right, top = point_to_bbox(lng, lat)
    nearest = list(idx.nearest((left, bottom, right, top), 2))
    """ print(nearest) """
    nearestlist = []

    dic ={}
    polygon =[]
    
    # for each id get all other properties from
    # rtee and add it to a list

    for item in nearest:
        nearestlist.append({
            'type': 'Feature',
            'geometry': rtreeid[item]['geometry'],
            'properties': rtreeid[item]['properties']
        })
        
        dic = rtreeid[item]['geometry']
        for key,value in dic.items():
            if key =='coordinates':
                lnglat =[]
                lnglat.append(value[0])
                lnglat.append(value[1])
        polygon.append(lnglat)
                
    for item in answer_CollectionpolyGon['features']:
        item['geometry']['coordinates'].append( polygon)
    """ print( answer_CollectionpolyGon) """
   # add nearestlist to a dictionary
   # to make it a geojson file
    answer_Collection['features'] = nearestlist
    # convert into JSON:
    convertedGeojson = json.dumps(answer_CollectionpolyGon)
    """ print( convertedGeojson) """
    # the result is a JSON string:
    # to be used as id in the frontend
def intersection(left,bottom,right,top):
  
    """ print(type( left)) """
   
    answer_Collection = {
        "type": "FeatureCollection",
        "features": []
    }
    idx, rtreeid = build_index()
    intersect = list(idx.intersection((left, bottom, right, top),objects=True))
    intersectid =[]
    for ids in intersect:
        intersectid.append(ids.id)
    intersectid = list(dict.fromkeys(intersectid))    
    
    nearestlist = []
    for item in intersectid:
        dic = rtreeid[item]['geometry']
        for key,value in dic.items():
            if key =='coordinates':
                lng = value[0]
                lat = value[1]
                flag = inboundingBox(bottom,left,top,right,lng,lat)
                if flag ==True:
                    nearestlist.append({
                    'type': 'Feature',
                    'geometry': rtreeid[item]['geometry'],
                    'properties': rtreeid[item]['properties']
                    })
      
    # add nearestlist to a dictionary
    # to make it a geojson file
    answer_Collection['features'] = nearestlist
    # convert into JSON:
    convertedGeojson = json.dumps(answer_Collection)
    # the result is a JSON string:
    # to be used as id in the frontend
    return convertedGeojson

def inboundingBox(x1, y1, x2,y2, x, y) : 
    if (x > x1 and x < x2 and y > y1 and y < y2) : 
        return True
    else : 
        return False



    r = lambda: random.randint(0,255)
    """ print('#%02X%02X%02X' % (r(),r(),r())) """
    
def checkgeojson():
    json ={
  "type": "Feature",
  "geometry": {
    "type": "Point",
    "coordinates": [125.6, 10.1]
  },
  "properties": {
    "name": "Dinagat Islands"
  }
} 



def nearestNeighborsRoads(lng,lat):
    coords = Point((lng,lat))
    left,right,bottom, top = coords.bounds
    nearest = list(idx2.nearest((left,right,bottom, top), 1))
    
    nearestlist = []
    for item in nearest:
        coords = rtreeroadid[item]['geometry']["coordinates"]
        listed = coords[0]
        nearestlist.append(listed[0])
    
    return nearestlist

def Travel(lng,lat,lng1,lat1,Graph):
    results = []
    answer_Collection = {
        "type": "FeatureCollection",
        "features": [ ]
    }
    lnglat = nearestNeighborsRoads(lng,lat)
    lnglat1 = nearestNeighborsRoads(lng1,lat1)
    print("nearest1")
    print(lnglat[0])
    print("nearest 2")
    print(lnglat1[0])
    path = nx.shortest_path(Graph, source = tuple(lnglat[0]), target = tuple(lnglat1[0]),weight = None, method = 'dijkstra')
    """ print(type(path)) """
    if isinstance(path, list):
        for point in path:
            results.append(list(point))
        """ print("did") """
        answer_Collection["features"].append({"type":"Feature",
          "properties": {},
            "geometry":
            {
            "type": "LineString",
            "coordinates": results
            }})
        """ print("done") """
        convertedGeojson = json.dumps(answer_Collection)
        with open('data.json', 'w') as outfile:
            json.dump(answer_Collection, outfile)
        return convertedGeojson
    else:
        answer = (path)
    return(answer)



def creategraphwithcities(Graph,path):
    data = load_data(path)
    feature = data['features']
    for row in feature:
        resultlist= tuple(row["geometry"]["coordinates"])
        
        lng = resultlist[1]
        lat = resultlist[0]
        another = (lng,lat)
        
        Graph.add_node(another)
    return Graph

def withinbox(lng,lat):
   
    top = 71.3577635769 # north lat
    left = -171.791110603 # west long
    right = -66.96466 # east long
    bottom =  18.91619 # south lat
    """ Accepts a list of lat/lng tuples. 
        returns the list of tuples that are within the bounding box for the US.
        NB. THESE ARE NOT NECESSARILY WITHIN THE US BORDERS!
    """
    flag = False
    
    if bottom <= lat <= top and left <= lng <= right:
        flag = True
        
    
    return flag

def findclosestRoad(path,Graph):
    data = load_data(path)
    count =0
    feature = data['features']
    for row in feature:
        """ resultlist= row["geometry"]["coordinates"] """
        result = row["properties"]       
        count+=1
        lng = result["LONGITUDE"]
        lat = result["LATITUDE"]
        
        if(withinbox(lng,lat)):
            anotherlist = (lng,lat)
            lnglat = nearestNeighborsRoads(lng,lat)
            length = len(lnglat)
            if length ==2:
            
                createedge = tuple(lnglat[1])
                Graph.add_edge(anotherlist,createedge)
                
            else:
                createedge = tuple(lnglat[0])
                Graph.add_edge(anotherlist,createedge)
    print("done")
    return Graph
                
    
def AddnewNodeToGraph():
    """ graphwithcities = creategraphwithcities(G2,populatedPlacespath)
    answer = findclosestRoad(populatedPlacespath,graphwithcities)
    G3 = answer.to_undirected() """
    

def FindBouningBox(path):
    data = load_data(path)
    feature = data['features']
    for row in feature:
        resultlist= row["geometry"]["coordinates"]
        for coord in resultlist:
            cood = coord[0]
            """ print(cood) """
            break
        break

        
        
   
if __name__ == '__main__':
    Travel(-78.0199,36.6796,-80.4969,34.8252,G2)
   
    
    
    
    
    
   
    
    
    
    
 
   

    
   
    
   
   