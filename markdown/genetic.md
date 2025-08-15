:title: Genetic Algorithms
:description: A genetic algorithm running in the browser.
:year: 2022
:month: 10
:day: 9
:math: true
:code: true

These particles are born in the left half of the screen, and are left to wander around... After some number of iterations, those who are in the right half of the canvas, **survive**, the others, are **killed**. Admittedly it's a rough world to live in, but that's life.

Each particle has a small neural network brain that takes 4 inputs: the distance from the particle to each wall. The neural network outputs 4 numbers that we use to compute a displacement in the x axis `$dx$` and a displacement in the y axis `$dy$`.

```latex
\tanh \left(
\begin{bmatrix}
    \text{top} \\
    \text{left} \\
    \text{bottom} \\
    \text{right}
\end{bmatrix}
\begin{bmatrix}
    w_{11} & w_{12} & w_{13} & w_{14} \\
    w_{21} & w_{22} & w_{23} & w_{24} \\
    w_{31} & w_{32} & w_{33} & w_{34} \\
    w_{41} & w_{42} & w_{43} & w_{44}
\end{bmatrix}
\right)
=
\begin{bmatrix}
    y_1 \\
    y_2 \\
    y_3 \\
    y_4
\end{bmatrix}
```

The displacements are computed arbitrarily as:

```latex
\left\{
\begin{array}{ll}
    dx = y_1 - y_2 \\
    dy = y_3 - y_4
\end{array}
\right.
```

When particles survive the death round, they are paired in groups of 2 to produce a child particle. The child particle's brain (*aka* neural network) is built by mixing the neural network parameters from each of its parents. More precisely, the neural network of the child inherits half the `$W$` parameters matrix from each of its parents. The parents and the child are then taken to the next round.

Interestingly, the parameters of each particle's brain are never trained per-se (for example with [gradient descent](https://en.wikipedia.org/wiki/Gradient_descent)), but simply built out of the parents brains. Another interesting fact is that particles are never told to go right; they don't even know how the output of their brain is being used. They have essentially *zero feedback* from the environment. However, since we only ever keep the particles that behaved in a certain way, i.e. went right, we end up with a population that has the sought-after characteristics.

This is the process of natural selection.

---

So, next time you see a Samara flying in the wind and wonder how smart nature is to develop these beautiful structures that optimize seed propagation; keep in mind, those who can't compete... ***will die***.

<center><canvas class="article-canvas" id="canvas" style="width: 50%;"></canvas></center>
<center>Epoch: <span id="status"></span></center>

## Population Size
<center><div id="population_size" style="width: 100%; height: 250px; margin: 30px 0px;"></div></center>

## Survival Ratio
<center><div id="survival_ratio" style="width: 100%; height: 250px; margin: 30px 0px;"></div></center>

<script src="https://cdnjs.cloudflare.com/ajax/libs/d3/7.9.0/d3.min.js" integrity="sha512-vc58qvvBdrDR4etbxMdlTt4GBQk1qjvyORR2nrsPsFPyrs+/u5c3+1Ct6upOgdZoIl7eq6k3a1UPDSNAQi/32A==" crossorigin="anonymous" referrerpolicy="no-referrer"></script>
<script src="/scripts/canvas.js"></script>
<script src="/scripts/plot.js"></script>
<script src="/scripts/matrix.js"></script>
<script src="/assets/genetic/genetic.js"></script>
