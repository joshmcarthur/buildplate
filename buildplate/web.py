"""
Provisions a JSON API endpoint for clients to access
Buildplate content via HTTP.
"""

import tempfile
import os
import buildplate.project as projects
from buildplate.mesh import MESH_FILE_EXTENSIONS

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 256 * 1024 * 1024


def filename_parts(filename):
    """
    Splits filename into its component parts
    """
    return filename.rsplit('.', 1)


def validate_filename(filename):
    """
    Validates that the uploaded file is in the list
    of permitted mesh extensions.
    """
    return '.' in filename and filename_parts(filename)[1].lower() in MESH_FILE_EXTENSIONS


def validation_error(message):
    """
    Cause Flask to return a 422 status message with the provided message.
    Message is assumed to be a string, but it doesn't have to be.
    """

    return {'error': message}, 422


@app.route("/api/projects")
def index():
    """ Lists all filepaths to STL files """
    return jsonify([project.dump() for project in projects.list_all()])



@app.route("/api/projects", methods=['POST'])
def create():
    """
    Create a new project using an STL file. The file must be provided
    and have an .stl extension. The file is saved to a tempfile, run
    through provisioning, and then the tempfile is removed.
    """

    file = request.files and request.files['mesh']
    if not file or (file and (file.filename == '' or not validate_filename(file.filename))):
        return validation_error("Mesh file must be provided")

    filename, extension = filename_parts(file.filename)

    _stream, destination = tempfile.mkstemp(
        prefix=filename, suffix=f".{extension.lower()}")
    file.save(destination)
    project = projects.provision(destination)
    os.unlink(destination)

    return project.dump(), 201
