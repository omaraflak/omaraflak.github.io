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