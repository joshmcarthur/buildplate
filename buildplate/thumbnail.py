""" Methods to generate thumbnail or preview images from 3D design files"""

import vtkplotlib as vpl
from stl.mesh import Mesh


def generate_thumbnail(infile, outfile, size=None):
    """Generate a thumbnail or previewfile into 'outfile' using the design file in 'infile'"""
    mesh = Mesh.from_file(infile)
    vpl.mesh_plot(mesh)

    # Front of design and slightly up
    vpl.view(camera_position=[0, -1, 0.5])
    vpl.save_fig(outfile, pixels=size or [1280, 1280], off_screen=True)
