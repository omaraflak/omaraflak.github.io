:title: Gravity
:description: Simulation of gravity with moving particles
:year: 2022
:month: 10
:day: 8
:math: true

This is a simulation of gravity using Newton's law of motion:

```latex
\sum{\overrightarrow{F}} = m\overrightarrow{a}
```

and Newton's law of gravity:

```latex
\overrightarrow{F_{a \rightarrow b}} = G \frac{m_a m_b}{d_{ab}^2} \overrightarrow{u_{ba}}
```

To make things interesting, I've set the particles to repulse themselves if they come too close together. You can play with that parameter using the slider below.

<div class="article-center-row article-block"><canvas id="canvas" style="width: 50%;"></canvas></div>
<div style="display: flex; align-items: center;">
    <span>Number of particles: </span>
    <input type="range" min="100" max="1000" value="500" id="total_particles">
    <span id="total_particles_placeholder">500</span>
</div>
<div style="display: flex; align-items: center;">
    <span>Repulsion distance: </span>
    <input type="range" min="0" max="200" value="50" id="min_distance">
    <span id="min_distance_placeholder">50</span>
</div>
<script src="/scripts/canvas.js"></script>
<script src="/scripts/matrix.js"></script>
<script src="/assets/gravity/gravity.js"></script>