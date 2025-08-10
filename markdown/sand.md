:title: Sand Cellular Automata
:description: A sand simulation using a cellular automata.
:year: 2024
:month: 1
:day: 25

This is a sand simulation based on a cellular automata. Each grain of sand is updated according to the value of its direct three bottom adjacent neighbors.

1. If the immediate bottom cell is empty, then the grain of sand falls in it.
2. If the bottom cell contains another grain of sand, then the grain of sand will either stay where it is, or fall on either side of that other grain of sand if any of the two cells are empty.


<canvas class="article-canvas" id="canvas"></canvas>
<script src="/scripts/canvas.js"></script>
<script src="/assets/sand/sand.js"></script>