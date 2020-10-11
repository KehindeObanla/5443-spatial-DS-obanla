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
idx = index.Index('eq-rtree')

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

    return (lng-offset,lat-offset,lng+offset,lat+offset)

def move_point(p,distance,feet=False):
    p[1] += float(distance) / 111111.0
    p[0] += float(distance) / (111111.0*(math.cos(10)))
    return p

def build_index():
    #(left, bottom, right, top)
    
    eqks = glob.glob("assignments\A04\Assets\json\earthquake_data\earthquakes\*.json")
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
                lng,lat,_ = row['geometry']['coordinates']
              #  earthquakeUniqueid[count] =row
                if lng < minlng:
                    minlng = lng
                if lat < minlat:
                    minlat = lat
                if lng > maxlng:
                    maxlng = lng
                if lat > maxlat:
                    maxlat = lat

                rect = point_to_bbox(lng,lat)
                idx.insert(count, rect)
                count += 1
            else:
                bad += 1
    #print(count)
    return idx,earthquakeUniqueid


 #returns a list of nearest neigh   
def nearestNeighbors(lng, lat):
    idForJson=0 # counter
    answer_Collection = {
        'type':"FeatureCollection",
        'features':[]
    }
    earthquakertree,rtreeid = build_index()
    nearest = list(earthquakertree.nearest((lng,lat,lng,lat),5))
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
    answer_Collection['feature'] = nearestlist
    idForJson+=1
    #returns geojson and a list of numbers 
    #to be used as id in the frontend
    return jsonify([str(idForJson),answer_Collection])



if __name__=='__main__':
     app.run(host='localhost', port=8080)
  
    