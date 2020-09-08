from flask import Flask
from flask import jsonify
from buildplate.folderstructure import list

app = Flask(__name__)

@app.route("/")
def hello_world():
  all = list()
  return jsonify(all)