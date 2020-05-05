import os
import torch
from math import cos, sin, exp, log, sqrt, atan, acos
from pytorch3d.io import load_obj, save_obj
from pytorch3d.structures import Meshes, Textures
from pytorch3d.utils import ico_sphere, torus

from extensions_utils import cube, cylinder, surface_of_revolution


DATA_FOLDER = os.path.join('data', 'meshes')
def locate_mesh(name:str):
    return os.path.join(DATA_FOLDER, name)

cylinder_mesh = cylinder(1, 2, 50, 10)
verts, faces = cylinder_mesh.get_mesh_verts_faces(0)
save_obj(locate_mesh('cylinder-5-1.obj'), verts, faces)

cube_mesh = cube(4)
verts, faces = cube_mesh.get_mesh_verts_faces(0)
save_obj(locate_mesh('cube-lv4.obj'), verts, faces)


def line(u):
    return 2*u

def vase(u):
    return 2 + acos(u)

def rev_exp(u):
    return 1 + exp(u)

def rev_log(u):
    return 1 + log(0.1 + u)

def rev_parabola(u):
    return u**2

def rev_hiperbole(u):
    return sqrt((u+1)**2 - 1)

def pseudo_sphere(u):
    return 4*atan(exp(u))

def rev_circle(u):
    return sqrt(1-u**2)

curves = {
    'cone': line,
    'paraboloid': rev_parabola,
    'rev_cos': vase,
    'rev_exp': rev_exp,
    'rev_log': rev_log,
    'hiperboloid': rev_hiperbole,
    'pseudo_sphere': pseudo_sphere,
    'rev_circle': rev_circle
}

for name, f in curves.items():
    rev_mesh = surface_of_revolution(f)
    verts, faces = rev_mesh.get_mesh_verts_faces(0)
    save_obj(locate_mesh('{}.obj'.format(name)), verts, faces)