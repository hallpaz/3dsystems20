import torch
from itertools import tee
from math import cos, pi, sin
from typing import Iterator, Optional, Tuple
from pytorch3d.structures.meshes import Meshes


# Make an iterator over the adjacent pairs: (-1, 0), (0, 1), ..., (N - 2, N - 1)
def _make_pair_range(N: int, start=-1) -> Iterator[Tuple[int, int]]:
    i, j = tee(range(start, N))
    next(j, None)
    return zip(i, j)

def cylinder(
    radius: float, height: float, sides: int, rings: int, closed=True, device: Optional[torch.device] = None
) -> Meshes:
    """
    Create vertices and faces for a torus.
    Args:
        r: base radius of the cylinder.
        h: height of the cylinder.
        sides: Number of angle divisions.
        rings: Number of height divisions.
        closed: Wether the top and bottom should be closed or not
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
    if closed:
        # bottom center
        verts.append([0, 0, -height/2])
        #top center
        verts.append([0, 0, height/2])

    faces = []
    for i0, i1 in _make_pair_range(sides):
        index0 = i0 % sides
        index1 = i1 % sides
        for j in range(rings-1):
            index00 = index0 + (j * sides)
            index01 = index0 + ((j+1) *sides)
            index10 = index1 + (j * sides)
            index11 = index1 + ((j+1) *sides)
            faces.append([index00, index10, index11])
            faces.append([index11, index01, index00])
    
    if closed:
        # close bottom and top of cylinder
        for i0, i1 in _make_pair_range(sides):
            index0 = i0 % sides
            index1 = i1 % sides
            faces.append([index0, len(verts)-2, index1])
            faces.append([index1 + (rings-1)*sides, len(verts)-1, index0 + (rings-1)*sides])
    
    verts_list = [torch.tensor(verts, dtype=torch.float32, device=device)]
    faces_list = [torch.tensor(faces, dtype=torch.int64, device=device)]
    return Meshes(verts_list, faces_list)