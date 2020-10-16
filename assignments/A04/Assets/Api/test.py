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

def finddistance():
    """ Description: return a distance between two points
        Params: 
            None
        Example: http://localhost:8080/distance/?lnglat=
    """
    lng,lat,lng1,lat1= -124.000,34.000 ,-124.0020,34.0020
    lnglat = (float(lng),float(lat))
    lnglat1 =(float(lng1),float(lat1))
    return haversine(lnglat, lnglat1, miles=True)
    
def load_data(path):
    """ Given a path, load the file and handle it based on its
        extension type. So far I have code for json and csv files.
    """
    _, ftype = os.path.splitext(path)   # get fname (_), and extenstion (ftype)

    if os.path.isfile(path):            # is it a real file?
        with open(path) as f:

            if ftype == ".json" or ftype == ".geojson":  # handle json
                data = f.read()
                if isJson(data):
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


CITIES = load_data(
    "assignments\\A04\\assets\\json\\countries_states\\major_cities.geojson")
STATES = load_data(
    "assignments\\A04\\assets\\json\\countries_states\\states.json")


def cities():
    """ Description: return a list of US state names
        Params:
            None
        Example: http://localhost:8080/cities
    """
    """ filter = request.args.get('filter',None) """
    results = []

    for city in CITIES["features"]:
        answers = {
                    "Name": city["properties"]["name"],
                    "Coordinates": city["geometry"]["coordinates"]
                    }
        results.append(answers)
    print(results[0])


def sub():
    filter = ''
    results = []
    if (filter):
        
        for city in CITIES["features"]:
            if filter.lower() == city["properties"]["name"].lower():
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
    print(results[0])
    return handle_response(results)

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
    
    
    return (jsonify(result))
     
def states():
    """ Description: return a list of US state names
        Params: 
            None
        Example: http://localhost:8080/states?filter=mis
    """
    filter ="texas"
   
    if filter:
        results = []
        for state in STATES:
            if filter.lower() == state['name'][:len(filter)].lower():
                results.append(state)
                print(state)
    else:
        results = STATES

if __name__=='__main__':
    test = finddistance()
    print(test, "is of type", type(test))