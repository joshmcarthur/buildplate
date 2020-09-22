""" Defines and manages project data models"""

import json
import pathlib
from shutil import copyfile
from os import path
from glob import glob
from marshmallow import Schema, fields, post_load
from buildplate.projects_dir import get_projects_dir, bootstrap
from buildplate.variant import Variant, VariantSchema
from buildplate.utils import sha1

MANIFEST_FILENAME = "manifest.json"


class Project:
    """ The base data model for a project. Has a root and a name, with zero or more variants. """

    def __init__(self):
        """ Define the attributes of the model """
        self.id = None
        self.name = None
        self.root = None
        self.variants = []

    def save(self, filename=MANIFEST_FILENAME):
        """ Convenience method to persist the project JSON to a manifest"""
        with open(path.join(self.root, filename), "w") as file:
            return json.dump(self.dump(), fp=file)

    def root_dir(self):
        """ Return a Path object of the root """
        return pathlib.Path(self.root)

    def dump(self):
        """ Convenience method to transform the project into it's Python object representation"""
        schema = ProjectSchema()
        return schema.dump(self)

    def images_dir(self, absolute=False):
        """ The path to the images directory for this project """
        images_dir = pathlib.Path("images")
        return images_dir if not absolute else self.root_dir().joinpath(images_dir)

    def files_dir(self, absolute=False):
        """ The path to the files directory for this project """
        files_dir = pathlib.Path("files")
        return files_dir if not absolute else self.root_dir().joinpath(files_dir)

    @staticmethod
    def from_file(manifest_path, filename=MANIFEST_FILENAME):
        """ Instantiates a project instance from a manifest file"""
        schema = ProjectSchema()
        project_dir = path.dirname(manifest_path)
        with open(path.join(project_dir, filename), 'r') as file:
            return schema.load(json.load(file))

    @staticmethod
    def from_dict(manifest, root=None):
        """ Instantiates a project from deserialized manifest dictionary"""
        project = Project()
        project.id = manifest["id"]
        project.name = manifest["name"]
        project.root = root or manifest["root"]
        project.variants = manifest["variants"]

        return project


class ProjectSchema(Schema):
    """ Represents the on-disk persisted format of a project"""
    id = fields.Str(required=True)
    name = fields.Str(required=True)
    root = fields.Str(required=True)
    variants = fields.List(fields.Nested(VariantSchema))

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
        for manifest_file in glob(path.join(root, "**", "manifest.json"), recursive=True)
    ]

def find_by_id(project_id, root=get_projects_dir()):
    """ Finds a project based on it's directory name """
    manifest_file = root.joinpath(project_id, "manifest.json")
    if not manifest_file.exists:
        raise f"Project {project_id} does not exist"

    return Project.from_file(manifest_file)


def provision(file):
    """ Copies a file into the project directory structure"""
    if not path.exists(file):
        raise ValueError("#{file} does not exist")

    bootstrap()

    project_id = sha1(file)
    basename = path.basename(file)
    filename, _extension = path.splitext(path.basename(file))
    container_path = pathlib.Path(get_projects_dir()).joinpath(project_id)

    if path.exists(container_path):
        raise ValueError(f"{file} already has a project (ID: {project_id})")

    project = Project()
    project.id = project_id
    project.name = filename
    project.root = container_path
    project.images_dir(absolute=True).mkdir(parents=True, exist_ok=True)
    project.files_dir(absolute=True).mkdir(parents=True, exist_ok=True)
    copyfile(file, project.files_dir(absolute=True).joinpath(basename))

    initial_variant = Variant()
    initial_variant.project = project
    initial_variant.build_file_path = project.files_dir().joinpath(basename)
    initial_variant.generate_preview_image()
    initial_variant.derive_metadata()
    project.variants = [initial_variant]

    project.save()

    return project
