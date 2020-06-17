# 3D Graphics Systems Course - IMPA 2020

#### Professor Luiz Velho
#### Hallison Paz, 1st year PhD student
---------

## Rendering a Scene with a Differentiable Renderer

The objective of this 2nd assignment is to render a scene using a differentiable renderer and exploit some capabilities of this system. We aim to render equirectangular panoramas, building a scene with a single sphere parameterized by latitude and longitude and setting the câmera in the center of the sphere.

### Modeling the Scene

First of all, we need to compute the geometry and texture coordinates for a sphere. We decided to use an equirectangular panorama as a bidimensional texture for the interior of the sphere, so it seems easier to parameterize the sphere in terms of latitude and longitude coordinates.

![Panorama Equirectangular; source: https://www.flickr.com/photos/101382486@N07/9688940322/in/photolist-NVEvL-FKxNb-8sNqz4-4xDge6-8sdop9-7EncwT-49Fsty-49GdCm-fLbmpd](img/panorama4.jpg)

For the geometry, we sample points uniformly as we increment the angles Phi and Theta in a spherical coordinate system. **0 <= Phi <= 2pi; 0 <= Theta < pi**. As the texture has a boundary and the sphere has not , we must be careful to achieve a good and meaningful result. Our strategy for a good mapping was:

1. We don't close the sphere in the poles. 
As we can see in line #2, we define an **epsilon**, so that **Theta** actually varies from **epsilon** to **pi-epsilon** and the vertices of the poles are sampled very close to each other, but are still considered different elements.

2. We duplicate the vertices located over the first meridian
For each parallel, we sample two vertices on the exact same location of the first sample, which is equivalent to consider that Phi belongs to the closed interval **[0, 2PI]**. We do that to simplify the computations of  the texture reconstruction on the surface, as it can be done with a linear interpolation.


<script src="https://gist.github.com/hallpaz/1c218e01c893c120b61a661731234c30.js"></script>

### Rendering the Scene
<!--stackedit_data:
eyJoaXN0b3J5IjpbMTA3NTI4NjMzNyw3ODgyMjA3NjcsLTEwNj
U0MjY0NTIsMTMzNTUzMDE4NCwtMTc5NjkzODE4OSwxNzU3NDgw
NTM5XX0=
-->