# 3D Graphics Systems Course - IMPA 2020

#### Professor Luiz Velho
#### Hallison Paz, 1st year PhD student
---------

## When AI renders a new Perspective in Graphics

This project builds on the previous assignments of 3D modeling and scene visualization using PyTorch3D, one of the AI graphics platforms available for free. 

> Our goal is to render a panoramic scene using a differentiable
> renderer and exploit the inverse rendering to augment a scene.

Most of the experiments can be found in the [rendering](https://colab.research.google.com/drive/1ggdaF0OFeAm9CTC1ZXiQFUnNxdgrrRWH?usp=sharing) or [de-rendering](https://colab.research.google.com/drive/16393ggQ6bzDhjda7pMBoMOAFluPzRSL-?usp=sharing) Google Colab notebooks. You can [download full results here](https://drive.google.com/drive/folders/1IUPjgpALrnlfuBMZir779LogZt2_ZxAR?usp=sharing).

### Motivation

As a personal goal, after some experience with traditional computer graphics and deep learning for computer vision using still images, I'm interested in understanding how to work with 3D data and artificial neural networks. From an external perspective, we see some very recent works applying deep learning in the context of omnidirectional representations [1, 2], which could lead to better VR/AR/XR applications and a huge impact the audiovisual industry. This perspective of the future and my previous experience working with panoramic images and studying how we could use such images for experiences in augmented or virtual reality makes this theme look promising. 

<iframe width="560" height="315" src="https://www.youtube.com/embed/WsWqGsZDkzY" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
*Layered Panorama Demo Application from* [3]

Rendering, or more specifically differentiable rendering, looks like a good topic to relate these areas as we'll see.

### Differentiable Rendering

Differentiable Rendering is not a technique but a whole field focused in rendering a 3D scene using a differentiable pipeline allowing gradients to flow back and forth 3D objects and images. This is a great way to join computer graphics and computer vision problems and to train self supervised models. A good work to understand the idea behind this field is [4], which states the rendering problem as the mapping:

f(theta) = I

"We define an observation function f(Θ) as the forward rendering process
that depends on the parameters Θ. The simplest optimization would solve for the parameters minimizing the difference between the rendered and observed image intensities, E(Θ) = ?f(Θ) − I?2."

We could calculate derivatives of the pixel values with respect to the forward rendering parameters. 

We could estimate object pose, calibrate camera parameters and even optimize illumination to match a target scene.

![Open DR](img/open_dr_earth.png)
*OpenDR example of optimization*

Both [] and [] create differentiable renderers by crafting approximations for the gradients of the non differentiable steps of the rendering pipeline, that is, the rasterization and Z-buffer.


### Experiments and Analysis


### Conclusion and next steps

As the works in this area are still very recent, we are subject to unexpected bugs as the one found in Pytorch3D.  Although ... we managed to complete the rendering step of our panoramic scene using the Soft Rasterizer 
-   ✓Parameterize rotations (quaternions?)
-   ✓Render new objects in panoramic environment

You can find the Keynote presented at the course below.

### References

[1] Michael Broxton, John Flynn, Ryan Overbeck, Daniel Erickson, Peter Hedman, Matthew DuVall, Jason Dourgarian, Jay Busch, Matt Whalen and Paul Debevec; **Immersive Light Field Video with a Layered Mesh Representation**. ACM Trans. Graph. 39, 4, Article 1 (July 2020).

[2] Daniel Martin, Ana Serrano and Belen Masia; Panoramic convolutions for 360º single-image saliency prediction. ```
CVPR Workshop on Computer Vision for Augmented and Virtual Reality, 2020.

[3] Carlos Eduardo Rocha, Diego Bretas, Hallison da Paz, Paulo Rosa, and Luiz Velho. "Framework para Aplicações em Plataformas Móveis usando Panoramas com Camadas". Technical Report TR-04-2014, IME, 2014. ([Portuguese only](http://www.visgraf.impa.br/Data/RefBib/PS_PDF/tr-042014/tr-04-2014.pdf))

[4] M. M. Loper and M. J. Black. **Opendr: An approximate differentiable renderer**. In European Conference on Computer Vision, pages 154–169. Springer, 2014.

[5] H. Kato, Y. Ushiku, and T. Harada. **Neural 3d mesh renderer**. In Proceedings ofthe IEEE Conference on Computer Vision and Pattern Recognition, pages 3907–3916, 2018.

[6] Liu, S., Li, T., Chen, W., Li, H.: **Soft rasterizer: A differentiable renderer for image-based 3d reasoning**. In: Proceedings of the IEEE International Conference on Computer Vision. pp. 7708–7717 (2019)

###### You may contact me at hallpaz@impa.br
<!--stackedit_data:
eyJoaXN0b3J5IjpbLTE1ODMxMDQ3MjIsMTMwMjY5MDA4NiwyOD
g4NDE3NjQsLTIxMzc5Mzc4OTEsMTc3MzIwMDg2MiwtNjg5NjE4
MTMyLDE4MzY4NTc4OTldfQ==
-->