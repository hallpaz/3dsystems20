import os
import torch
from math import cos, sin, exp, log, sqrt, atan, acos
from pytorch3d.io import load_obj, save_obj
from pytorch3d.structures import Meshes, Textures
from pytorch3d.utils import ico_sphere, torus

from extensions_utils import cube, cylinder, surface_of_revolution, equisphere


DATA_FOLDER = os.path.join('data', 'meshes')
def locate_mesh(name:str):
    return os.path.join(DATA_FOLDER, name)

def test_ylinder():
    cylinder_mesh = cylinder(1, 2, 50, 10)
    verts, faces = cylinder_mesh.get_mesh_verts_faces(0)
    save_obj(locate_mesh('cylinder-5-1.obj'), verts, faces)

def test_cube():
    cube_mesh = cube(4)
    verts, faces = cube_mesh.get_mesh_verts_faces(0)
    save_obj(locate_mesh('cube-lv4.obj'), verts, faces)


def test_revolution():
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

def test_equisphere():
    v, f, uv = equisphere(80, 40)
    sphere_mesh = Meshes([v], [f])
    verts, faces = sphere_mesh.get_mesh_verts_faces(0)
    save_obj(locate_mesh('equisphere.obj'), verts, faces)
    write_obj(locate_mesh('tex_equisphere.obj'), verts, faces, uv)


def write_obj(filepath, verts, faces, uvs):
    with open(filepath, 'w') as obj:
        obj.write('mtllib panorama.mtl\n\n')
        for v in verts:
            obj.write('v {} {} {}\n'.format(v[0], v[1], v[2]))

        for uv in uvs:
            obj.write('vt {} {}\n'.format(uv[0], uv[1]))
        obj.write('usemtl material_1\n')
        for f in faces:
            obj.write('f {0}/{0} {1}/{1} {2}/{2}\n'.format(f[0]+1, f[1]+1, f[2]+1))

if __name__ == "__main__":
    test_equisphere()