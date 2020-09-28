from flask import Flask
from flask import request
from flask import jsonify
from flask_cors import CORS
from rtree import index
app = Flask(__name__)
CORS(app)











if __name__ == '__main__':
      app.run(host='0.0.0.0', port=8080)