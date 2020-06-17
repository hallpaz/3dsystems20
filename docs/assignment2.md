# 3D Graphics Systems Course - IMPA 2020

### Professor Luiz Velho
### Hallison Paz, 1st year PhD student
---------

## Assignment 2 - Rendering a Scene with a Differentiable Renderer

The objective of this assignment is to render a scene using a differentiable renderer and exploit some capabilities of this system. We aim to render equirectangular panoramas, building a scene with a single sphere parameterized by latitude and longitude and setting the câmera in the center of the sphere.

### Modeling the Scene

First of all, we need to compute the geometry and texture coordinates for a sphere. We decided to use an equirectangular panorama as a bidimensional texture for the interior of the sphere, so it seems easier to parameterize the sphere in terms of latitude and longitude coordinates.

![Panorama Equirectangular; source: https://www.flickr.com/photos/101382486@N07/9688940322/in/photolist-NVEvL-FKxNb-8sNqz4-4xDge6-8sdop9-7EncwT-49Fsty-49GdCm-fLbmpd](img/panorama4.jpg)

For the geometry, we sample points uniformly as we increment the 
<script src="https://gist.github.com/hallpaz/1c218e01c893c120b61a661731234c30.js"></script>

### Rendering the Scene
<!--stackedit_data:
eyJoaXN0b3J5IjpbLTE3NjcyNDUzNDIsMTMzNTUzMDE4NCwtMT
c5NjkzODE4OSwxNzU3NDgwNTM5XX0=
-->