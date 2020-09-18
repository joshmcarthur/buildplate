""" Defines and manages project data models"""

import json
import pathlib
from shutil import copyfile
from os import path
from glob import glob
from marshmallow import Schema, fields, post_load
from buildplate.projects_dir import get_projects_dir, bootstrap
from buildplate.variant import Variant, VariantSchema

MANIFEST_FILENAME = "manifest.json"


class Project:
    """ The base data model for a project. Has a root and a name, with zero or more variants. """

    def __init__(self):
        """ Define the attributes of the model """
        self.name = None
        self.root = None
        self.variants = []

    def save(self, filename=MANIFEST_FILENAME):
        """ Convenience method to persist the project JSON to a manifest"""
        with open(path.join(self.root, filename), "w") as fp:
            return json.dump(self.dump(), fp=fp)

    def dumps(self):
        """ Convenience method to transform the project into it's JSON representation"""
        schema = ProjectSchema()
        return schema.dump(self)
    
    def images_dir(self):
        return pathlib.Path(self.root).joinpath("images")

    def files_dir(self):
        return pathlib.Path(self.root).joinpath("files")

    @staticmethod
    def from_file(manifest_path, filename=MANIFEST_FILENAME):
        """ Instantiates a project instance from a manifest file"""
        schema = ProjectSchema()
        project_dir = path.dirname(manifest_path)
        with open(path.join(project_dir, filename), 'r') as f:
            return schema.load(json.load(f))

    @staticmethod
    def from_dict(manifest, root=None):
        """ Instantiates a project from deserialized manifest dictionary"""
        project = Project()
        project.name = manifest["name"]
        project.root = root or manifest["root"]
        project.variants = manifest["variants"]


class ProjectSchema(Schema):
    """ Represents the on-disk persisted format of a project"""
    name = fields.Str(required=True)
    root = fields.Str(required=True)
    variants = fields.Nested(VariantSchema)

    @post_load
    def make_project(self, data, **_kwargs):  # pylint: disable=no-self-use
        """ Invoked by the schema to transform a deserialized dict into a Project instance"""
        return Project.from_dict(data)


def list_all(root=get_projects_dir()):
    """ Lists all STL files within the directory identified by the argument 'root',
        defaulting to the project directory
    """
    return [
        Project.from_file(manifest_file)
        for manifest_file in glob(path.join(root, "**", "*.stl"), recursive=True)
    ]


def provision(file):
    """ Copies a file into the project directory structure"""
    if not path.exists(file):
        raise ValueError("#{file} does not exist")

    bootstrap()

    basename = path.basename(file)
    filename, _extension = path.splitext(path.basename(file))
    container_path = pathlib.Path(get_projects_dir()).joinpath(filename)

    project = Project()
    project.name = filename
    project.root = container_path
    project.images_dir().mkdir(parents=True, exist_ok=True)
    project.files_dir().mkdir(parents=True, exist_ok=True)
    copyfile(file, project.files_dir().joinpath(basename))

    initial_variant = Variant()
    initial_variant.project = project
    initial_variant.build_file_path = project.files_dir().joinpath(basename)
    project.variants = [initial_variant]

    project.save()

    return project
