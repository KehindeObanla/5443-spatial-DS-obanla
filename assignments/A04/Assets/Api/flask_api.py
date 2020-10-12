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


app = Flask(__name__)
CORS(app)
idx = index.Index()

@app.route("/token", methods=["GET"])
def getToken():
    """ getToken: this gets mapbox token
    """
    token = {'token':'pk.eyJ1Ijoia2VoaW5kZW9iYW5sYSIsImEiOiJja2ZuNm42b3kxamwzMndrdXIyNHkzOG8wIn0.qe4TrmVMMfi1Enpcvk5GfQ'}

    return token


def validateJSON(jsonData):
    try:
        json.loads(jsonData)
    except ValueError as err:
        return False
    return True

def point_to_bbox(lng,lat,offset=.001):
    #(left, bottom, right, top)

    return (float(lng-offset),float(lat-offset),float(lng+offset),float(lat+offset))

def move_point(p,distance,feet=False):
    p[1] += float(distance) / 111111.0
    p[0] += float(distance) / (111111.0*(math.cos(10)))
    return p

def build_index():
    #(left, bottom, right, top)
    
    eqks = glob.glob("assignments\A04\Assets\json\earthquake_data\earthquakes\*.json")
    del eqks[300:840]
    count = 0
    bad = 0
    earthquakeUniqueid = {}

    for efile in eqks:
        minlat = 999
        minlng = 999
        maxlat = -999
        maxlng = -999
        with open(efile,'r',encoding='utf-8') as f:
            data = f.readlines()

        for row in data[2:]:
            row = row.strip()
            row = row.strip(",")
            if validateJSON(row):
                row = json.loads(row)
                lng,lat,_ = row["geometry"]["coordinates"]
                earthquakeUniqueid[count] =row
                if lng < minlng:
                    minlng = lng
                if lat < minlat:
                    minlat = lat
                if lng > maxlng:
                    maxlng = lng
                if lat > maxlat:
                    maxlat = lat

                left, bottom, right, top = point_to_bbox(lng,lat)
                idx.insert(count, (left, bottom, right, top))
                count += 1
            else:
                bad += 1
        """  print(count) """
    return idx,earthquakeUniqueid


 #returns a list of nearest neigh   
def nearestNeighbors(lng, lat):
    answer_Collection = {
        "type":"FeatureCollection",
       "features":[]
    }
    
    idx,rtreeid = build_index()
    left, bottom, right, top = point_to_bbox(lng,lat)
    nearest = list(idx.nearest(( left, bottom, right, top ),2))
    print (nearest)
    nearestlist = []
    # for each id get all other properties from
    #rtee and add it to a list

    for item in nearest:
        nearestlist.append({
            'type':'Feature',
            'geometry':rtreeid[item]['geometry'],
            'properties':rtreeid[item]['properties']
        })
   # add nearestlist to a dictionary
   #to make it a geojson file
    answer_Collection['features'] =nearestlist
    # convert into JSON:
    convertedGeojson = json.dumps(answer_Collection)
    # the result is a JSON string: 
    #to be used as id in the frontend
    return convertedGeojson
@app.route('/click/')
def click():
    lng, lat = request.args.get("lngLat",None).split(",")
    return nearestNeighbors(float(lng), float(lat))


if __name__=='__main__':
    app.run(host='localhost', port=8080)
  
    
        
   
    