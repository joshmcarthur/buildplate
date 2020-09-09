""" Manages the design library folder structure"""
from shutil import copyfile
from os import mkdir, path
from glob import glob
from library_dir import get_library_dir, bootstrap


def list_all(root=get_library_dir()):
    """ Lists all STL files within the directory identified by the argument 'root',
        defaulting to the library directory
    """
    return glob(root.join("**/*.stl"), recursive=True)

def provision(file):
    """ Copies a file into the library directory structure"""
    if not path.exists(file):
        raise ValueError("#{file} does not exist")

    bootstrap()
    container_path = path.join(get_library_dir(), path.basename(file))

    mkdir(container_path)
    mkdir(container_path.join("files"))
    mkdir(container_path.join("images"))
    copyfile(file, container_path.join(file))
