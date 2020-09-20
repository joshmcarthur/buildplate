""" Helpers for working with 3D design files"""
from stl.mesh import Mesh

MESH_FILE_EXTENSIONS = {'stl'}


def dimensions(infile):
    """Accepts a 3D mesh file as infile, and returns the x,y,z dimensions of the object in mm"""
    mesh = Mesh.from_file(infile)
    return [
        float(mesh.x.max()) - float(mesh.x.min()),
        float(mesh.y.max()) - float(mesh.y.min()),
        float(mesh.z.max()) - float(mesh.z.min())
    ]


def volume(infile):
    """Accepts a 3D mesh file as inline, and returns the volume of the object in cubic mm"""
    mesh = Mesh.from_file(infile)
    vol, _, _ = mesh.get_mass_properties()

    return float(vol)
