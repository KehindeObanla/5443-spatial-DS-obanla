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
"""
  _   _ _____ _     ____  _____ ____
 | | | | ____| |   |  _ \| ____|  _ \
 | |_| |  _| | |   | |_) |  _| | |_) |
 |  _  | |___| |___|  __/| |___|  _ <
 |_| |_|_____|_____|_|   |_____|_| \_\

"""
def logg(data):
    with open("logg.log","w") as logger:
        logger.write(json.dumps(data,indent=4))

def handle_response(data,params=None,error=None):
    """ handle_response
    """
    success = True
    if data:
        if not isinstance(data,list):
            data = [data]
        count = len(data)
    else:
        count = 0
        error = "Data variable is empty!"

    
    result = {"success":success,"count":count,"results":data,"params":params}

    if error:
        success = False
        result['error'] = error
    
    
    return jsonify(result)

def formatHelp(route):
    """ Gets the __doc__ text from a method and formats it
        for easier viewing. Whats "__doc__"? This text
        that your reading is!!
    """
    help = globals().get(str(route)).__doc__
    if help != None:
        help = help.split("\n")
        clean_help = []
        for i in range(len(help)):
            help[i] = help[i].rstrip()
            if len(help[i]) > 0:
                clean_help.append(help[i])
    else:
        clean_help = "No Help Provided."
    return clean_help

def isFloat(string):
    """ Helper method to test if val can be float
        without throwing an actual error.
    """
    try:
        float(string)
        return True
    except ValueError:
        return False

def isJson(data):
    """ Helper method to test if val can be json
        without throwing an actual error.
    """
    try:
        json.loads(data)
        return True
    except ValueError:
        return False


def load_data(path):
    """ Given a path, load the file and handle it based on its
        extension type. So far I have code for json and csv files.
    """
    _, ftype = os.path.splitext(path)   # get fname (_), and extenstion (ftype)
  
    if os.path.isfile(path):            # is it a real file?
        with open(path) as f:
            
            if ftype == ".json" or ftype == ".geojson":# handle json
                data = f.read()
                if isJson(data):
                    return json.loads(data)
                
            elif ftype == ".csv":       # handle csv with csv reader
                with open(path, newline='') as csvfile:
                    data = csv.DictReader(csvfile)
                
                    return list(data)
    return None
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
    
    eqks = glob.glob("assignments\\A04\\Assets\\json\\earthquake_data\\earthquakes\\*.json")
    del eqks[350:840]
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
    nearest = list(idx.nearest(( left, bottom, right, top ),5))
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
    #nearest neghibour on click
"""
  ____    _  _____  _      ____    _    ____ _  _______ _   _ ____
 |  _ \  / \|_   _|/ \    | __ )  / \  / ___| |/ / ____| \ | |  _ \
 | | | |/ _ \ | | / _ \   |  _ \ / _ \| |   | ' /|  _| |  \| | | | |
 | |_| / ___ \| |/ ___ \  | |_) / ___ \ |___| . \| |___| |\  | |_| |
 |____/_/   \_\_/_/   \_\ |____/_/   \_\____|_|\_\_____|_| \_|____/

Helper classes to act as our data backend.
"""

STATES = load_data("assignments\\A04\\assets\\json\\countries_states\\states.json")
STATE_BBOXS = load_data("assignments\\A04\\assets\\json\\countries_states\\us_states_bbox.csv")
CITIES = load_data("assignments\\A04\\assets\\json\\countries_states\\major_cities.geojson")
idx = index.Index()
"""
   ____   ___  _   _ _____ _____ ____  
  |  _ \ / _ \| | | |_   _| ____/ ___| 
  | |_) | | | | | | | | | |  _| \___ \ 
  |  _ <| |_| | |_| | | | | |___ ___) |
  |_| \_\\___/ \___/  |_| |_____|____/ 
"""
@app.route("/token", methods=["GET"])
def getToken():
    """ getToken: this gets mapbox token
    """
    token = {'token':'pk.eyJ1Ijoia2VoaW5kZW9iYW5sYSIsImEiOiJja2ZuNm42b3kxamwzMndrdXIyNHkzOG8wIn0.qe4TrmVMMfi1Enpcvk5GfQ'}

    return token

@app.route("/", methods=["GET"])
def getRoutes():
    """ getRoutes: this gets all the routes to display as help for developer.
    """
    routes = {}
    for r in app.url_map._rules:
        
        routes[r.rule] = {}
        routes[r.rule]["functionName"] = r.endpoint
        routes[r.rule]["help"] = formatHelp(r.endpoint)
        routes[r.rule]["methods"] = list(r.methods)

    routes.pop("/static/<path:filename>")
    routes.pop("/")

    response = json.dumps(routes,indent=4,sort_keys=True)
    response = response.replace("\n","<br>")
    return "<pre>"+response+"</pre>"

@app.route('/geo/direction/')
def get_direction():
    """ Description: Return the direction between two lat/lon points.
        Params: 
            lng1 (float) : point 1 lng
            lat1 (float) : point 1 lat
            lng2 (float) : point 1 lat
            lat2 (float) : point 1 lat

        Example: http://localhost:8080/geo/direction/?lng1=-98.4035194716&lat1=33.934640760&lng2=-98.245591004&lat2=34.0132220288
    """
    lng1 = request.args.get('lng1',None)
    lat1 = request.args.get('lat1',None)
    lng2 = request.args.get('lng2',None)
    lat2 = request.args.get('lat2',None)

    b = bearing((float(lng1),float(lat1)), (float(lng2),float(lat2)))

    return handle_response([{"bearing":b}],{'lat1':lat1,'lng1':lng1,'lat2':lat2,'lng2':lng2})

@app.route('/click/')
def click():
    """ Description: return a list of US nearest negihbours
        Params: 
            None
        Example:http://localhost:8080/click/?lngLat="
    """
    lng, lat = request.args.get("lngLat",None).split(",")
    return nearestNeighbors(float(lng), float(lat))

@app.route('/cities', methods=["GET"])
def cities():
    """ Description: return a list of US ciyies names and long lat
        Params: 
            None
        Example: http://localhost:8080/cities?filter=mis
    """
    filter = request.args.get('filter',None)
    results = []
    if (filter):
        
        for city in CITIES["features"]:
            if filter.lower() == city["properties"]["name"][:len(filter)].lower():
                answers = {
                    "Name": city["properties"]["name"],
                    "Coordinates": city["geometry"]["coordinates"]
                    }
                results.append(answers)
    else:
        for city in CITIES["features"]:
            answers = {
                    "Name": city["properties"]["name"],
                    "Coordinates": city["geometry"]["coordinates"]
                    }
            results.append(answers)

    return handle_response(results)
""" using halversine function to find distance """
@app.route('/distance/', methods=["GET"])
def finddistance():
    """ Description: return a distance between two points
        Params: 
            None
        Example: http://localhost:8080/distance/?lnglat=
    """
    lng,lat,lng1,lat1= request.args.get('lnglat',None).split(",")
    checkformiORkm=request.args.get('lnglat',None).split(";")
    lng,lat,lng1,lat1=checkformiORkm[0].split(",")
    mile = checkformiORkm[1]
    if(mile =='mile'):
        lnglat = (float(lng),float(lat))
        lnglat1 =(float(lng1),float(lat1))
        answer = haversine(lnglat, lnglat1, miles=True)
        return str( answer )
  
    else:
        lnglat = (float(lng),float(lat))
        lnglat1 =(float(lng1),float(lat1))
        answer = haversine(lnglat, lnglat1, miles=False)
        return str( answer )

@app.route('/states', methods=["GET"])
def states():
    """ Description: return a list of US state names
        Params: 
            None
        Example: http://localhost:8080/states?filter=mis
    """
    filter = request.args.get('filter',None)
   
    if filter:
        results = []
        for state in STATES:
            if filter.lower() == state['name'][:len(filter)].lower():
                results.append(state)
    else:
        results = STATES

    return handle_response(results)

@app.route('/state_bbox/', methods=["GET"])
def state_bbox():
    """ Description: return a bounding box for a us state
        Params: 
            None
        Example: http://localhost:8080/state_bbox/<statename>
    """
    state = request.args.get('state',None)
    
    if not state:
        results = STATE_BBOXS
        return handle_response(results)
    
    state = state.lower()
    
    results = []
    for row in STATE_BBOXS:
        if row['name'].lower() == state or row['abbr'].lower() == state:
            row['xmax'] = float(row['xmax'])
            row['xmin'] = float(row['xmin'])
            row['ymin'] = float(row['ymin'])
            row['ymax'] = float(row['ymax'])
            results = row
            

    return handle_response(results)


if __name__=='__main__':
    app.run(host='localhost', port=8080,debug=True)
  
    
        
   
    