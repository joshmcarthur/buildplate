import vtkplotlib as vpl
from stl.mesh import Mesh


def generate_thumbnail(infile, outfile, size=[1280,1280]):
    mesh = Mesh.from_file(infile)
    vpl.mesh_plot(mesh)

    # Front of design and slightly up
    vpl.view(camera_position=[0, -1, 0.5])
    vpl.save_fig(outfile, pixels=size)
