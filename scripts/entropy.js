const xValues = [];
const yValues = [];
const numPoints = 300;
const xMin = -0.5;
const xMax = 1.5;
const step = (xMax - xMin) / (numPoints - 1);

for (let i = 0; i < numPoints; i++) {
    const x = xMin + i * step;
    xValues.push(x);
    yValues.push(-Math.log(x));
}

functionPlot({
    target: '#negative-log',
    xAxis: {
        label: 'x',
        domain: [-3, 6]
    },
    yAxis: {
        label: 'y=-log(x)',
        domain: [-2, 3.5]
    },
    annotations: [
        {
            x: 1,
            text: 'x = 1'
        }
    ],
    grid: true,
    data: [{ fn: '-log(x)' }]
})