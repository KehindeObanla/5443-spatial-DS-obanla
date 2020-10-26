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


""" checks a valid geojson """
def checkgeojson(dic,value,key ="type"):
        answer ="True"
        if(key =="type" and value == "Feature"):
            flag = checkfeature(dic)
            if(flag ==True):
                return answer
            else:
                return "invalid geojson"
            
        elif(key =="type" and value == "FeatureCollection"):
            flag2 = checkFeatureCollection(dic)
            if(flag2 ==True):
                return answer
            else:
                return "invalid geojson"
        else:
            return "invalid geojson"
           
        
""" checks a valid feature geojson """
def checkfeature(dic):
    featuretype =["Point", "LineString", "Polygon", "MultiPoint", "MultiLineString","MultiPolygon"]
    propertyflag = False
    count = 0
    if("type" not in dic):
        count-=1
    if("geometry" not in dic):
        count-=1
    for key, value in dic.items() :
        print(value)
        if(key =="type" and value == "Feature"):
            count+=1
        elif(key =="geometry" and isinstance(value ,dict)):
            count+=1
            print(value)
            if("type" not in value):
                count-=1
            if("coordinates" not in value):
                count-=1
            for key, value in value.items() :
               
                if(key == "type"and value  not in featuretype):
                    count-=1
                if(key =="coordinates"and isinstance(value ,list)):
                    count+=1
       
        elif(key =="properties" and isinstance(value ,dict)):
            propertyflag=True
            count+=1
    
    if(count ==4 and propertyflag == True):
        return True
    elif(count ==3 and propertyflag == False):
        return True
    else:
        return False
    
""" checks a valid featurecollection geojson """
def checkFeatureCollection(dic):
    flag = False
    count =0
    if("type" not in dic):
        count-=1
    for key, value in dic.items() :
        if(key =="type" and value == "FeatureCollection"):
            count+=1
        if(key =="features"):
            if(isinstance(value,list)):
                length = len(value)
                print(length)
                for feat in value:
                    flag = checkfeature(feat)
                    if (flag == False):
                        return False
    if(flag == True and count == 1):
        return True

if __name__ == '__main__':

    dic ={
            "type": "Feature",
            "geometry": {
            "type": "Point",
            "coordinates": [125.6, 10.1,]
            },
            "properties": {
                "name": "Dinagat Islands"
            }
        } 
    dics ={
            "type": "Feature",
            "geometry": {
            "type": "Point"
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
    """ dic3 ={
        { "type": "Feature",
         "geometry": {
           "type": "Polygon",
           "coordinates": [
             [ [100.0, 0.0], [101.0, 0.0], [101.0, 1.0],
               [100.0, 1.0], [100.0, 0.0] ]
             ]
         }}
    } """
    dic4 ={ "type": "FeatureCollection",
    "features": [
      { "type": "Feature",
        "geometry": {"type": "Point", "coordinates": [102.0, 0.5]},
        "properties": {"prop0": "value0"}
        },
      { "type": "Feature",
        "geometry": {
          "type": "LineString",
          "coordinates": [
            [102.0, 0.0], [103.0, 1.0], [104.0, 0.0], [105.0, 1.0]
            ]
          },
        "properties": {
          "prop0": "value0",
          "prop1": 0.0
          }
        },
      { "type": "Feature",
         "geometry": {
           "type": "Polygon",
           "coordinates": [
             [ [100.0, 0.0], [101.0, 0.0], [101.0, 1.0],
               [100.0, 1.0], [100.0, 0.0] ]
             ]
         },
         "properties": {
           "prop0": "value0",
           "prop1": {"this": "that"}
           }
         }
       ]
     }
    location={
        "type": "FeatureCollection",
  "features": [
    { "type": "Feature",
      "geometry": {"coordinates": [80.2066734649931, 13.0187039189613]},
      "properties": {
          "assetStatus": "FULL",
          "id": 1747,
          "item": "53 Trailer"
      }
    },
    { "type": "Feature",
      "geometry": {"coordinates": [ 80.2072495864164, 13.0191043036246]},
      "properties": {
          "assetStatus": "EMPTY",
          "id": 1746,
          "item": "53 Trailer"
      }
    },
    { "type": "Feature",
      "geometry": { "coordinates": [ 80.2067574402883, 13.0191983952581]},
      "properties": {
          "assetStatus": "LOADED",
          "id": 1745,
          "item": "53 Trailer"
      }
    }
  ]
}
    answer = checkgeojson(dic4,"FeatureCollection")
    print(answer)
        