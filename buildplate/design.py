from stl.mesh import Mesh


def dimensions(infile):
    mesh = Mesh.from_file(infile)
    return [
        mesh.x.max() - mesh.x.min(),
        mesh.y.max() - mesh.y.min(),
        mesh.z.max() - mesh.z.min()
    ]

def volume(infile):
  mesh = Mesh.from_file(infile)
  volume, _, _ = mesh.get_mass_properties()

  return volume
