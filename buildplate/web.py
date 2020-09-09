"""
Provisions a JSON API endpoint for clients to access
Buildplate content via HTTP.
"""

from flask import Flask, jsonify
from folderstructure import list_all

app = Flask(__name__)

@app.route("/")
def index():
    """ Lists all filepaths to STL files """
    all_designs = list_all()
    return jsonify(all_designs)
