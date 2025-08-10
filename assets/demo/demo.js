// 1. Define the function you want to plot
function myFunction(x) {
    return x * x; // Example: y = x^2
}

// 2. Generate data points for the plot
const xValues = [];
const yValues = [];
const numPoints = 100; // Number of points to sample
const xMin = -10;
const xMax = 10;
const step = (xMax - xMin) / (numPoints - 1);

for (let i = 0; i < numPoints; i++) {
    const x = xMin + i * step;
    xValues.push(x);
    yValues.push(myFunction(x));
}

// 3. Create the trace object
const trace = {
    x: xValues,
    y: yValues,
    mode: 'lines', // To connect the points with lines
    name: 'y = x^2'
};

// 4. Define the layout (optional)
const layout = {
    title: 'Plot of y = x^2',
    xaxis: {
        title: 'x'
    },
    yaxis: {
        title: 'y'
    }
};

// 5. Plot the data
Plotly.newPlot('plotDiv', [trace], layout);