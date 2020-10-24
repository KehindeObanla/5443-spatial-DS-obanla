import sys
import os
from rtree import index
from flask import Flask
from flask import request
from flask import jsonify
from json import loads
from flask_cors import CORS
import glob
import json
import math
import re


def checkgeojson(dic,value,key ="type"):
        if(key =="type" and value == "Feature"):
            flag = checkfeature(dic)
            print("Feature")
            print (flag)
        elif(key =="type" and value == "FeatureCollection"):
            flag2 = checkFeatureCollection(dic)
            print("FeatureCollection")
            print (flag2)
        else:
            print("invalid geojson")
           
        

def checkfeature(dic):
    featuretype =["Point", "LineString", "Polygon", "MultiPoint", "MultiLineString","MultiPolygon"]
    count = 0
    for key, value in dic.items() :
        if(key =="type" and value == "Feature"):
            count+=1
        if(key =="geometry" and isinstance(value ,dict)):
            count+=1
            for key, value in value.items() :
                if(key == "type" and value in featuretype):
                    count+=1
                if(key =="coordinates"and all(isinstance(x, (int, float)) for x in value)):
                    count+=1
        if(key =="properties" and isinstance(value ,dict)):
            count+=1
    print(count)
    if(count ==5):
        return True
    else:
        return False

def checkFeatureCollection(dic):
    count =0
    for key, value in dic.items() :
        if(key =="type" and value == "FeatureCollection"):
            count+=1
        if(key =="features" and isinstance(value[0] ,dict)):
            count+=1
            flag = checkfeature(value[0])
            if(flag == True):
                return True
    return False

if __name__ == '__main__':
  
    dic ={
  "type": "Featureing",
  "geometry": {
    "type": "Point",
    "coordinates": [125.6, 10.1,]
  },
  "properties": {
    "name": "Dinagat Islands"
  }
} 
   
    dic2 ={'type': 'FeatureCollection',
        'features': [
        {
        'type': 'Feature',
        'geometry': {
        'type': 'Polydgon',
        'coordinates': []
        }}]
        }
    dic3 ={{ "type": "Feature",
         "geometry": {
           "type": "Polygon",
           "coordinates": [
             [ [100.0, 0.0], [101.0, 0.0], [101.0, 1.0],
               [100.0, 1.0], [100.0, 0.0] ]
             ]
         }}
        
    checkgeojson(dic,"FeatureColletion")