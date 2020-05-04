import os
import math
import models
import torch
from pytorch3d.io import load_obj, save_obj
from pytorch3d.structures import Meshes, Textures
from pytorch3d.utils import ico_sphere, torus

DATA_FOLDER = os.path.join('data', 'meshes')
def locate_mesh(name:str):
    return os.path.join(DATA_FOLDER, name)

# cylinder_mesh = models.cylinder(1, 2, 20, 10)
# verts, faces = cylinder_mesh.get_mesh_verts_faces(0)
# save_obj(locate_mesh('cylinder-2-4.obj'), verts, faces)

cube_mesh = models.cube(4)
verts, faces = cube_mesh.get_mesh_verts_faces(0)
save_obj(locate_mesh('cube-lv4.obj'), verts, faces)


def line(u):
    return 1/2*u

def vase(u):
    return 2 + math.cos(u)
# rev_mesh = models.surface_of_revolution(vase, height=4)
# verts, faces = rev_mesh.get_mesh_verts_faces(0)
# save_obj(locate_mesh('vase.obj'), verts, faces)