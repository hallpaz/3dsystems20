# 3D Graphics Systems Course - IMPA 2020

#### Professor Luiz Velho
#### Hallison Paz, 1st year PhD student
---------

## Rendering a Scene with a Differentiable Renderer

The objective of this 2nd assignment is to render a scene using a differentiable renderer and exploit some capabilities of this system. We aim to render equirectangular panoramas, building a scene with a single sphere parameterized by latitude and longitude and setting the câmera in the center of the sphere. You can find the [full source code here](https://github.com/hallpaz/3dsystems20/blob/master/Rendering%20Panoramas.ipynb).

### Modeling the Scene

First of all, we need to compute the geometry and texture coordinates for a sphere. A valid concern about textures is the possibility of distortion due to the mapping. We decided to parameterize the sphere in terms of latitude and longitude coordinates, as well as use an equirectangular panorama as a bidimensional texture for the interior of the sphere. With this representation, we have an image that takes into account the distortion of the surface.

![Panorama Equirectangular; source: https://www.flickr.com/photos/101382486@N07/9688940322/in/photolist-NVEvL-FKxNb-8sNqz4-4xDge6-8sdop9-7EncwT-49Fsty-49GdCm-fLbmpd](img/panorama4.jpg)

For the geometry, we sample points uniformly as we increment the angles Phi and Theta in a spherical coordinate system. **0 <= Phi <= 2pi; 0 <= Theta < pi**. As the texture has a boundary and the sphere has not , we must be careful to achieve a good and meaningful result. Our strategy for a good mapping was:

##### Geometry  and Texture Coordinates

1. We don't close the sphere in the poles. 
As we can see in line #2, we define an **epsilon**, so that **Theta** actually varies from **epsilon** to **pi-epsilon** and the vertices of the poles are sampled very close to each other, but are still considered different elements.

2. We duplicate the vertices located over the first meridian
For each parallel, we sample two vertices on the exact same location of the first sample, which is equivalent to consider that Phi belongs to the closed interval **[0, 2PI]**. We do that to simplify the computations of  the texture reconstruction on the surface, as it can be done with a linear interpolation. Lines #19 to #25 implement this approach.

<script src="https://gist.github.com/hallpaz/1c218e01c893c120b61a661731234c30.js"></script>


**Mesh Triangulation**

We triangulate the mesh by connecting vertices on adjacents parallels and meridians over the surface. We choose the order of the vertices such that each face has a clockwise (CW) winding order. This way, the normals point to the interior of the surface where we wish to locate our camera.

<script src="https://gist.github.com/hallpaz/e4ab7e85c37d221cdd9e2381b8d541a5.js"></script>

In the end of the function we convert the lists of data into Pytorch tensors, so we have a data structure compatible with the operations 

### Rendering the Scene

[This tutorial](https://pytorch3d.org/tutorials/render_textured_meshes) in the PyTorch3D website shows how to set up a renderer to render a textured mesh. We use it as a starting point to our experiments.

##### Loading mesh data

The [tutorial] shows how to load an obj file into memory with material data to render a textured surface.  Our first approach was to try to write the computed the geometry of the mesh to an obj file with texture information. However, we discovered that the library does not support saving a mesh with texture coordinates yet and [it does not intent to add this feature soon](https://github.com/facebookresearch/pytorch3d/issues/151). To solve this problem, we figured how to use the Texture class out of the source code.

##### Setting the camera inside the sphere



#### Investigating the unexpected results

##### Toy texture

##### Moving the câmera in the tutorial

##### Cropping the mesh

##### Looking for alternatives renderers

We tried to use the Tensorflow Graphics to render a mesh, but we couldn't find information on how to render a textured mesh and it didn't appear we could achieve it on time. Our second alternative was the Open Differentiable Renderer (OpenDR).

### Conclusion



<!--stackedit_data:
eyJoaXN0b3J5IjpbMzcwNDE2MzM4LC0xMDIzMTYzNTI1LC00Nj
IzNDI2NywtMTc5MDg3MDY0MSwtNTc3NDMwNTI2LC0zNDM1ODM1
OTIsMTEzMTY1Mzk0NSwtOTMzOTE2NzYsNzg4MjIwNzY3LC0xMD
Y1NDI2NDUyLDEzMzU1MzAxODQsLTE3OTY5MzgxODksMTc1NzQ4
MDUzOV19
-->