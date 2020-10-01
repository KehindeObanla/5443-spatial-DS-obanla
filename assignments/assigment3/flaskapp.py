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


def get_stardata():
    filedata = './stardata/stars8.json'
    if os.path.isfile(filedata):
        with open(filedata,'r') as f:
            data =f.read()
    else:
        return jsonify({"Error":"star8.json not there!!"})

    return loads(data)

def loadstarInRtree(starloc):
    starRtree = rtree.index.Index()
    starTreeId ={}
    for data in starloc["features"]:
        if data["type"] == "Feature" and data["geometry"]["type"] =="Point":
            starCoordinate =(data["geometry"]["coordinates"][0],data["geometry"]["coordinates"][1],
            data["geometry"]["coordinates"][0],data["geometry"]["coordinates"][1])
            starid =(int(data["id"]))
            starRtree.insert(starid,starCoordinate)
            starTreeId[starid] = data
    return [starRtree,starTreeId]    

    

@app.route('/')
def index():
    return 'This is the base route'

@app.route('/click/')
def click():
    global count 
    count =0
    lng, lat = request.args.get("lngLat",None).split(",")  
    star8data = get_stardata()
    [starRtree,starTreeId] = loadstarInRtree(star8data)
    answer_Collection = {
        'type':'FeatureCollection',
        'feature':[]
    }
    nearest = list(starRtree.nearest((float(lng),float(lat),float(lng),float(lat)),3))
    nearestlist =[]
    for item in nearest:
        nearestlist.append({
            'type':'feature',
             'geometry':starTreeId[item]['geometry'],
             'properties':starTreeId[item]['properties']
        })
    answer_Collection['features'] = nearestlist
    count += 1
    return jsonify(request.json.get[str(count),answer_Collection])
    ####################################################



   

if __name__ == '__main__':
    app.run(host='localhost', port=8080)