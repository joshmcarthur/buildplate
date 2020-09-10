""" Manages the design library folder structure"""
from shutil import copyfile
from os import mkdir, path
from glob import glob
from buildplate.library_dir import get_library_dir, bootstrap


def list_all(root=get_library_dir()):
    """ Lists all STL files within the directory identified by the argument 'root',
        defaulting to the library directory
    """
    return glob(path.join(root, "**", "*.stl"), recursive=True)

def provision(file):
    """ Copies a file into the library directory structure"""
    if not path.exists(file):
        raise ValueError("#{file} does not exist")

    bootstrap()
    filename, file_ext = path.splitext(path.basename(file))
    container_path = path.join(get_library_dir(), filename)

    mkdir(container_path)
    mkdir(path.join(container_path, "files"))
    mkdir(path.join(container_path, "images"))
    copyfile(file, path.join(container_path, f'{filename}{file_ext}'))

    return container_path
