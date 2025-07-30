:title: Brownian Motion
:description: Particles performing a random walk.
:year: 2025
:month: 7
:day: 28

These particles are following a random walk, or brownian motion. At each time step, we get a random direction in space for each particle and move it towards that direction.

```latex
\left\{
\begin{align*}
&\theta \sim U(0, 1) \\
&x_{t+1} = x_t + r \cos(2\pi\theta) \\
&y_{t+1} = y_t + r \sin(2\pi\theta)
\end{align*}
\right.
```

<canvas id="canvas" style="width: 100%; overflow-x: auto;"></canvas>

## Mean Squared Displacement

This is the [mean squared displacement](https://en.wikipedia.org/wiki/Mean_squared_displacement) over time. It is the average distance of a particle to its initial starting point (here, the center of the canvas).

```latex
MSD = \frac{1}{n} \sum_{x,y} = (x_t - x_0)^2 + (y_t - y_0)^2
```

<center><div id="mean_squared_displacement" style="width: 100%; margin: 30px 0px;"></div></center>

<script src="https://cdnjs.cloudflare.com/ajax/libs/d3/7.9.0/d3.min.js" integrity="sha512-vc58qvvBdrDR4etbxMdlTt4GBQk1qjvyORR2nrsPsFPyrs+/u5c3+1Ct6upOgdZoIl7eq6k3a1UPDSNAQi/32A==" crossorigin="anonymous" referrerpolicy="no-referrer"></script>
<script src="../scripts/canvas.js"></script>
<script src="../scripts/plot.js"></script>
<script src="../scripts/brownian.js"></script>