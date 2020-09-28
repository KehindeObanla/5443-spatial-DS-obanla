from flask import Flask
from flask import request
from flask import jsonify
from flask_cors import CORS
from rtree import index
app = Flask(__name__)
CORS(app)


coordinate = {
    "type": "Feature",
    "geometry": {
        "type":"point",
        "coordinates":[
            [1402528.63585071451962,7491973.552016104571521]
        ]
    },
    "properties": {
        "name": "Country",
       
    }
    
}
@app.route('/')
def indexs():
    return 'This is the base route'

@app.route('/click/')
def click():
    # lat = request.args.get("lat",None)
    # lng = request.args.get("lng",None)
    # lnglat = request.args.get("lnglat",None)
    lng,lat = request.args.get("lngLat",None).split(",")
    coordinate["coordinates"] = request.args.get("lnglat",None)
    idx = index.Index()
    left, bottom, right, top = (
        lng, 
        lat, 
        lng, 
        lat)
    idx.insert(0, (left, bottom, right, top), obj=coordinate)
    hits = list(idx.nearest((lng, lat, lng, lat), 3, objects=True))
    return hits

if __name__ == '__main__':
      app.run(host='localhost', port=8080)