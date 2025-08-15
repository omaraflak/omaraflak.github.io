:title: Wolfram Cellular Automata
:description: A demo of Wolfram's elementary cellular automata.
:year: 2024
:month: 1
:day: 27
:math: true

Wolfram elementary cellular automata are a fascinating piece of mathematics. We start with a grid of cells, where all cells are in an ***off*** state, except the middle cell of the first row, which is ***on***. Then, we proceed and apply the following rule to compute the state of all cells below the first row.

![rules](/assets/automata/automata.svg)

This is saying that for a given cell, we look at the three adjacent cells above it, and depending on their state the current cell will be either *on* or *off*.

As you can see, the three adjacent top cells can be in `$2^3=8$` possible configurations. Therefore there is `$2^8=256$` possible ***rules*** that we could apply. This is just one of them. It's called rule 30, because `$(00011110)_{2} = (30)_{10}$`.

You can read more about this simple cellular automata on Wolfram's website:

[](https://mathworld.wolfram.com/ElementaryCellularAutomaton.html)

Below is a simulation of the above rule, and somehow this very simple rule creates those intricate patterns that seem regular but also chaotic! Enter a rule number below to see them all!

<canvas class="article-canvas" id="canvas"></canvas>
<center>
<div>
    <span class="text">Rule: </span>
    <input type="number" min="0" max="255" value="30" id="rule">
</div>
</center>
<script src="/scripts/canvas.js"></script>
<script src="/assets/automata/automata.js"></script>
