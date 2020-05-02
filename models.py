from itertools import tee
from math import cos, pi, sin
from typing import Iterator, Optional, Tuple

import torch
from pytorch3d.structures.meshes import Meshes


# Make an iterator over the adjacent pairs: (-1, 0), (0, 1), ..., (N - 2, N - 1)
def _make_pair_range(N: int, start=-1) -> Iterator[Tuple[int, int]]:
    i, j = tee(range(start, N))
    next(j, None)
    return zip(i, j)


def torus(
    r: float, R: float, sides: int, rings: int, device: Optional[torch.device] = None
) -> Meshes:
    """
    Create vertices and faces for a torus.
    Args:
        r: Inner radius of the torus.
        R: Outer radius of the torus.
        sides: Number of inner divisions.
        rings: Number of outer divisions.
        device: Device on which the outputs will be allocated.
    Returns:
        Meshes object with the generated vertices and faces.
    """
    if not (sides > 0):
        raise ValueError("sides must be > 0.")
    if not (rings > 0):
        raise ValueError("rings must be > 0.")
    device = device if device else torch.device("cpu")

    verts = []
    for i in range(rings):
        # phi ranges from 0 to 2 pi (rings - 1) / rings
        phi = 2 * pi * i / rings
        for j in range(sides):
            # theta ranges from 0 to 2 pi (sides - 1) / sides
            theta = 2 * pi * j / sides
            x = (R + r * cos(theta)) * cos(phi)
            y = (R + r * cos(theta)) * sin(phi)
            z = r * sin(theta)
            # This vertex has index i * sides + j
            verts.append([x, y, z])

    faces = []
    for i0, i1 in _make_pair_range(rings):
        index0 = (i0 % rings) * sides
        index1 = (i1 % rings) * sides
        for j0, j1 in _make_pair_range(sides):
            index00 = index0 + (j0 % sides)
            index01 = index0 + (j1 % sides)
            index10 = index1 + (j0 % sides)
            index11 = index1 + (j1 % sides)
            if 0 in [index00, index01, index10, index11]:
                print('Torus', [index00, index10, index11], [index11, index01, index00])
            faces.append([index00, index10, index11])
            faces.append([index11, index01, index00])

    verts_list = [torch.tensor(verts, dtype=torch.float32, device=device)]
    faces_list = [torch.tensor(faces, dtype=torch.int64, device=device)]
    return Meshes(verts_list, faces_list)


def cylinder(
    radius: float, height: float, sides: int, rings: int, device: Optional[torch.device] = None
) -> Meshes:
    """
    Create vertices and faces for a torus.
    Args:
        r: base radius of the cylinder.
        h: height of the cylinder.
        sides: Number of angle divisions.
        rings: Number of height divisions.
        device: Device on which the outputs will be allocated.
    Returns:
        Meshes object with the generated vertices and faces.
    """
    if not (sides > 0):
        raise ValueError("sides must be > 0.")
    if not (rings > 0):
        raise ValueError("rings must be > 0.")
    device = device if device else torch.device("cpu")

    verts = []
    for h in range(rings):
        z = height * h/(rings-1) - height/2
        for i in range(sides):
            # theta ranges from 0 to 2 pi (sides - 1) / sides
            theta = 2 * pi * i / sides
            x = radius * cos(theta)
            y = radius * sin(theta)
            verts.append([x, y, z])
    # bottom center
    verts.append([0, 0, -height/2])
    #top center
    verts.append([0, 0, height/2])

    faces = []
    for i0, i1 in _make_pair_range(sides):
        index0 = i0 % sides
        index1 = i1 % sides
        # print(index0, index1)
        for j in range(rings-1):
            index00 = index0 + (j * sides)
            index01 = index0 + ((j+1) *sides)
            index10 = index1 + (j * sides)
            index11 = index1 + ((j+1) *sides)
            faces.append([index00, index10, index11])
            faces.append([index11, index01, index00])
    # close bottom and top of cylinder
    for i0, i1 in _make_pair_range(sides):
        index0 = i0 % sides
        index1 = i1 % sides
        faces.append([index0, len(verts)-2, index1])
        faces.append([index1 + (rings-1)*sides, len(verts)-1, index0 + (rings-1)*sides])
    

    verts_list = [torch.tensor(verts, dtype=torch.float32, device=device)]
    faces_list = [torch.tensor(faces, dtype=torch.int64, device=device)]
    return Meshes(verts_list, faces_list)

# TODO: convert to parametric representation
def coeur(x, y, z):
    return (x**2 + (9/4)*y**2 + z**2 - 1)**3 - x**2 * z**3 - (9/80)*y**2 * z**3


# Vertex coordinates for a level 0 cube.
_half_size = 0.50
_cube_verts0 = [
    [-0.50, 0.50, 0.50],
    [-0.50, -0.50, 0.50],
    [0.50, -0.50, 0.50],
    [0.50, 0.50, 0.50],

    [-0.50, 0.50, -0.50],
    [-0.50, -0.50, -0.50],
    [0.50, -0.50, -0.50],
    [0.50, 0.50, -0.50]
]


# Faces for level 0 ico-sphere
_cube_faces0 = [
    [0, 1, 2],
    [2, 3, 0],

    [7, 6, 5],
    [4, 7, 5],
    
    [6, 3, 2],
    [3, 6, 7],

    [4, 5, 0],
    [0, 5, 1],

    [3, 4, 0],
    [4, 3, 7],

    [2, 1, 5],
    [5, 6, 2],
]

def cube(level=0, device = None):
    """
    Create verts and faces for a unit cube, with all faces oriented
    consistently.
    Args:
        level: integer specifying the number of iterations for subdivision
                of the mesh faces. Each additional level will result in four new
                faces per face.
        device: A torch.device object on which the outputs will be allocated.
    Returns:
        Meshes object with verts and faces.
    """
    if device is None:
        device = torch.device("cpu")
    if level < 0:
        raise ValueError("level must be >= 0.")
    if level == 0:
        verts = torch.tensor(_cube_verts0, dtype=torch.float32, device=device)
        faces = torch.tensor(_cube_faces0, dtype=torch.int64, device=device)

    return Meshes(verts=[verts], faces=[faces])

def surface_of_revolution(generatrix, sides = 20, rings = 10, height = 1, device = None):
    """
    Create vertices and faces for surface of revolution.
    TODO: Args:
        generatirx: para.
        sides: Number of angle divisions.
        rings: Number of height divisions.
        device: Device on which the outputs will be allocated.
    Returns:
        Meshes object with the generated vertices and faces.
    """
    if not (sides > 0):
        raise ValueError("sides must be > 0.")
    if not (rings > 0):
        raise ValueError("rings must be > 0.")
    device = device if device else torch.device("cpu")

    verts = []
    for h in range(rings):
        z = height * h/(rings-1)
        for i in range(sides):
            # theta ranges from 0 to 2 pi (sides - 1) / sides
            theta = 2 * pi * i / sides
            f = generatrix(z)
            x = f * cos(theta)
            y = f * sin(theta)
            verts.append([x, y, z])
    # bottom center
    verts.append([0, 0, 0])
    #top center
    verts.append([0, 0, height])

    faces = []
    for i0, i1 in _make_pair_range(sides):
        index0 = i0 % sides
        index1 = i1 % sides
        # print(index0, index1)
        for j in range(rings-1):
            index00 = index0 + (j * sides)
            index01 = index0 + ((j+1) *sides)
            index10 = index1 + (j * sides)
            index11 = index1 + ((j+1) *sides)
            faces.append([index00, index10, index11])
            faces.append([index11, index01, index00])
    # close bottom and top of cylinder
    for i0, i1 in _make_pair_range(sides):
        index0 = i0 % sides
        index1 = i1 % sides
        faces.append([index0, len(verts)-2, index1])
        faces.append([index1 + (rings-1)*sides, len(verts)-1, index0 + (rings-1)*sides])
    

    verts_list = [torch.tensor(verts, dtype=torch.float32, device=device)]
    faces_list = [torch.tensor(faces, dtype=torch.int64, device=device)]
    return Meshes(verts_list, faces_list)
