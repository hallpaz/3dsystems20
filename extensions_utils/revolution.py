import torch
from .commom import make_pair_range
from math import cos, pi, sin
from typing import Iterator, Optional, Tuple
from pytorch3d.structures.meshes import Meshes


def surface_of_revolution(generatrix, sides = 50, rings = 10, height = 1, closed=True, device = None):
    """
    Create vertices and faces for surface of revolution.
    TODO: Args:
        generatirx: ...
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
        u = height * h/(rings-1)
        # z = height * h/(rings-1)
        for i in range(sides):
            # theta ranges from 0 to 2 pi (sides - 1) / sides
            theta = 2 * pi * i / sides
            f = generatrix(u)
            x = u * cos(theta)
            y = u * sin(theta)
            verts.append([x, y, f])
    
    if closed:
        # bottom center
        verts.append([0, 0, 0])
        #top center
        verts.append([0, 0, generatrix(height)])

    faces = []
    for i0, i1 in make_pair_range(sides):
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
    
    if closed:
        # close bottom and top of cylinder
        for i0, i1 in make_pair_range(sides):
            index0 = i0 % sides
            index1 = i1 % sides
            faces.append([index0, len(verts)-2, index1])
            faces.append([index1 + (rings-1)*sides, len(verts)-1, index0 + (rings-1)*sides])

    verts_list = [torch.tensor(verts, dtype=torch.float32, device=device)]
    faces_list = [torch.tensor(faces, dtype=torch.int64, device=device)]
    return Meshes(verts_list, faces_list)