from shutil import copyfile
from os import mkdir, path
from glob import glob
from buildplate.store import get_library_dir, bootstrap

def list(root = get_library_dir()):
  return glob(root.join("**/*.stl"), recursive=True)

def provision(file):
    if not path.exists(file):
        raise ValueError("#{file} does not exist")

    bootstrap()
    container_path = path.join(get_library_dir(), path.basename(file))

    mkdir(container_path)
    mkdir(container_path.join("files"))
    mkdir(container_path.join("images"))
    copyfile(file, container_path.join(file))
