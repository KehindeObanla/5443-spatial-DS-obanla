from flask import Flask
from flask import request
from flask import jsonify
from json import loads
from os import path
from flask_cors import CORS
import rtree 
import json
import os
import sys

def main():
    filedata ='.../data/1996_3.json'
    if os.path.isfile(filedata):
        with open(filedata,'r') as f:
            data =f.read()
           
    else:
        return jsonify({"Error":"1996_3 not there!!"})
   
    parsed = json.loads(data)
           
    print (json.dumps(parsed, indent=2, sort_keys=True))


main()
 