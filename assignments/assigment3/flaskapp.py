from flask import Flask
from flask import request
from flask import jsonify
from flask_cors import CORS
import os,sys
import json
from rtree import index

app = Flask(__name__)
CORS(app)

def get_countries():
    data_file = '../assiggments3/countries.geo.json'
    if os.path.isfile(data_file):
        with open(data_file,'r') as f:
            data = f.read()
    else:
        return jsonify({"Error":"countries.geo.json not there!!"})

    return json.loads(data)

@app.route('/')
def index():
    return 'This is the base route'

@app.route('/click/')
def click():







# if __name__ == '__main__':
#       app.run(host='0.0.0.0', port=8080)