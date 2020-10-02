from flask import Flask
from flask import request
from flask import jsonify
from json import loads
from os import path
from flask_cors import CORS
import rtree 
import json
import os

app = Flask(__name__)
CORS(app)
#gets earthquake data from a json file
def get_earthquakeData():
    filedata = 'assignments/assigment3/data/1996_3.json'
    if os.path.isfile(filedata):
        with open(filedata,'r') as f:
            data =f.read()
    else:
        return jsonify({"Error":"1996_3 not there!!"}),404
    return json.loads(data)
#loads earthquke data to rtree with 
#a uniqueue id
def loadAiportintoRtree(earthquakedata):
     # creats rtree index
    earthquakeTree = rtree.index.Index()
    earthquakeUniqueid = {}
    id = 10
  
    for data in earthquakedata['features']:
        lon =data['geometry']['coordinates'][0]
        lat = data['geometry']['coordinates'][1]
        earthquakeUniqueid[id] =data
        earthquakeTree.insert(id,(float(lat),float(lon),float(lat),float(lon)))
        id+=1
    return earthquakeTree,earthquakeUniqueid
#base route
@app.route('/')
def index():
    return 'This is the base route'
#on click creates a bounding box
# with lat and long
@app.route('/click/')
def click():
    lng, lat = request.args.get("lngLat",None).split(",")
    maxx = float(float(lng) + 0.002) # The max coords from bounding rectangles
    minx = float(float(lng) - 0.002)
    maxy = float(float(lat) + 0.002)
    miny = float(float(lat) - 0.002)
    left, bottom, right, top = (minx, miny, maxx, maxy)
    earthquakedata =  get_earthquakeData() # gets earthquake data
    idForJson=0 # counter
    #gets tree id and rtree filled with earthquake data
    earthquakertree,rtreeid = loadAiportintoRtree(earthquakedata) 
    answer_Collection = {
        'type':"FeatureCollection",
        'features':[]
    }
     #stores the id of the closest earthquakes
    nearest = list(earthquakertree.nearest((left,bottom,right,top),5))
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
    #print(answer_Collection)
    return jsonify([str(idForJson),answer_Collection])
if __name__ == '__main__':
    app.run(host='localhost', port=8080)