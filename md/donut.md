:title: Donut
:description: How to create a spinning donut with math.
:year: 2022
:month: 10
:day: 8

Although this spinning donut is pretty impressive, it is quite easy to obtain using basic linear algebra. I'm going to show you how.

<center><canvas id="canvas" style="width: 200px; height: 200px; background-color: black; margin: 30px 0px;"></canvas></center>

The first step is to sample points from the surface of a 3D donut. We can do this by rotating a circle sitting on the plane $(x, y)$ centered at $(c,0,0)$ around the $y$ axis.

Sampling the circle points can be done using polar coordinates:

```latex
\left\{
\begin{array}{ll}
    x = r cos(\theta) + c, \quad \theta \in [0, 2 \pi] \\
    y = r sin(\theta) \\
    z = 0
\end{array}
\right.
```

Once we have the circle, we can rotate it around the $y$ axis using a 3D rotation matrix:

```latex
R_y(\theta) =
\begin{bmatrix}
    cos(\theta) & 0 & sin(\theta) \\
    0 & 1 & 0 \\
    -sin(\theta) & 0 & cos(\theta)
\end{bmatrix}
```

This will get you points on the donut surface. You can now multiply these points by a rotation matrix that rotates around all three axes to get the animation.

<script src="../scripts/canvas.js"></script>
<script src="../scripts/matrix.js"></script>
<script src="../scripts/donut.js"></script>