import torch
from .commom import make_pair_range
from math import cos, pi, sin
from typing import Iterator, Optional, Tuple
from pytorch3d.structures.meshes import Meshes
import numpy as np


# def equisphere(meridians = 20, parallels = 10, r = 1, device = None):
#     """
#     Create vertices and faces for surface of revolution.
#     TODO: Args:
#         generatirx: ...
#         meridians: Number of angle divisions.
#         parallels: Number of height divisions.
#         device: Device on which the outputs will be allocated.
#     Returns:
#         Meshes object with the generated vertices and faces.
#     """
#     if not (meridians > 0):
#         raise ValueError("sides must be > 0.")
#     if not (parallels > 0):
#         raise ValueError("rings must be > 0.")
#     device = device if device else torch.device("cpu")

#     verts = []
#     for m in range(meridians):
#         theta = m * pi/meridians
#         z = r * cos(theta)
#         for p in range(parallels):
#             phi = p * 2*pi/parallels
#             x = r * sin(theta) * cos(phi)
#             y = r * sin(theta) * sin(phi)
#             verts.append([x, y, z])

#     faces = []
#     for i0, i1 in make_pair_range(meridians):
#         index0 = i0 % meridians
#         index1 = i1 % meridians
#         # print(index0, index1)
#         for j in range(parallels-1):
#             index00 = index0 + (j * meridians)
#             index01 = index0 + ((j+1) * meridians)
#             index10 = index1 + (j * meridians)
#             index11 = index1 + ((j+1) * meridians)
#             faces.append([index00, index10, index11])
#             faces.append([index11, index01, index00])

#     verts_list = [torch.tensor(verts, dtype=torch.float32, device=device)]
#     faces_list = [torch.tensor(faces, dtype=torch.int64, device=device)]
#     return Meshes(verts_list, faces_list)


def equisphere(meridians = 180, parallels = 90, r = 1, device = None):
    """
    Create vertices and faces for surface of revolution.
    TODO: Args:
        generatirx: ...
        meridians: Number of angle divisions.
        parallels: Number of height divisions.
        device: Device on which the outputs will be allocated.
    Returns:
        Meshes object with the generated vertices and faces.
    """
    if not (meridians > 0):
        raise ValueError("sides must be > 0.")
    if not (parallels > 0):
        raise ValueError("rings must be > 0.")
    device = device if device else torch.device("cpu")

    epsilon = 0.00005
    verts = []
    verts_uv = []

    theta = epsilon
    for p in range(parallels):
        theta = p * (pi - 2*epsilon)/(parallels-1) + epsilon
        for m in range(meridians):
            phi = m * 2*pi/meridians
            
            u = phi/(2*pi)
            v = 1.0 - theta/pi
            verts_uv.append(np.array([u,v]))
            verts.append([
                -r*sin(theta)*sin(phi), r*cos(theta), r*sin(theta)*cos(phi)
            ])
        # replicating point for texturing
        phi = 0.0
        u = 1.0
        v = 1.0 - theta/pi
        verts_uv.append(np.array([u,v]))
        verts.append([
                -r*sin(theta)*sin(phi), r*cos(theta), r*sin(theta)*cos(phi)
        ])

    faces = []
    faces_uv = []
    for p in range(parallels-1):
        for m in range(meridians):
            # if p+1 < parallels:
            faces.append([
                p*(meridians+1) + m, 
                (p+1)*(meridians+1) +m, 
                p*(meridians+1) + m+1
            ])
            faces.append([
                    p*(meridians+1) + m+1, 
                    (p+1)*(meridians+1) + m,
                    (p+1)*(meridians+1) + m+1
                ])
    
            # faces_uv.append((verts_uv[p*(meridians+1) + m] + 
            #     verts_uv[(p+1)*(meridians+1) +m] +
            #     verts_uv[p*(meridians+1) + m+1])/3)
            # faces_uv.append((verts_uv[p*(meridians+1) + m+1] + 
            #     verts_uv[(p+1)*(meridians+1) + m] +
            #     verts_uv[(p+1)*(meridians+1) + m+1])/3)
            

    verts_list = torch.tensor(verts, dtype=torch.float32, device=device)
    faces_list = torch.tensor(faces, dtype=torch.int64, device=device)
    verts_uv_list = torch.tensor(verts_uv, dtype=torch.float32, device=device)
    # faces_uv_list = torch.tensor(faces_uv, dtype=torch.float32, device=device)

    return verts_list, faces_list, verts_uv_list, 