functionPlot({
    target: '#xor-plot',
    grid: true,
    xAxis: { domain: [-1, 2] },
    yAxis: { domain: [-1, 2] },
    data: [
        {
            points: [
                [0, 0],
                [0, 1],
                [1, 0],
                [1, 1],
            ],
            fnType: 'points',
            graphType: 'scatter'
        },
        {
            fn: '0.5*x+0.2'
        },
        {
            graphType: 'text',
            location: [0, 0],
            text: '(0,0)',
            color: 'black'
        },
        {
            graphType: 'text',
            location: [0, 1],
            text: '(0,1)',
            color: 'blue'
        },
        {
            graphType: 'text',
            location: [1, 0],
            text: '(1,0)',
            color: 'blue'
        },
        {
            graphType: 'text',
            location: [1, 1],
            text: '(1,1)',
            color: 'black'
        }
    ]
})