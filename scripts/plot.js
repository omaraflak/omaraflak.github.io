/**
 * SimplePlot.js - A lightweight D3.js line plotting library
 * 
 * Usage:
 * const plot = new SimplePlot('myDiv');
 * plot.plot([1, 2, 3, 4, 5]); // y-only data
 * plot.plot([1, 2, 3], [10, 20, 15]); // x, y data
 * plot.addData(6); // add single y point
 * plot.addData(4, 25); // add x, y point
 */

class SimplePlot {
    constructor(elementId, options = {}) {
        this.elementId = elementId;
        this.container = d3.select(`#${elementId}`);

        // Get container dimensions
        const containerNode = this.container.node();
        const containerRect = containerNode.getBoundingClientRect();
        const containerWidth = containerRect.width || containerNode.offsetWidth || 800;
        const containerHeight = containerRect.height || containerNode.offsetHeight || 400;

        // Default options
        this.options = {
            width: containerWidth,
            height: containerHeight,
            margin: { top: 0, right: 0, bottom: 25, left: 50 },
            strokeColor: '#2563eb',
            strokeWidth: 1,
            pointRadius: 1,
            showPoints: true,
            animationDuration: 0,
            ...options
        };

        // Calculate inner dimensions
        this.width = this.options.width - this.options.margin.left - this.options.margin.right;
        this.height = this.options.height - this.options.margin.top - this.options.margin.bottom;

        // Initialize data
        this.data = [];

        // Initialize SVG
        this.initSVG();
    }

    initSVG() {
        // Clear existing content
        this.container.selectAll('*').remove();

        // Create SVG
        this.svg = this.container
            .append('svg')
            .attr('width', this.options.width)
            .attr('height', this.options.height);

        // Create main group
        this.g = this.svg
            .append('g')
            .attr('transform', `translate(${this.options.margin.left}, ${this.options.margin.top})`);

        // Create scales
        this.xScale = d3.scaleLinear().range([0, this.width]);
        this.yScale = d3.scaleLinear().range([this.height, 0]);

        // Create line generator
        this.line = d3.line()
            .x(d => this.xScale(d.x))
            .y(d => this.yScale(d.y))
            .curve(d3.curveLinear);

        // Create axes groups
        this.xAxisGroup = this.g.append('g')
            .attr('class', 'x-axis')
            .attr('transform', `translate(0, ${this.height})`);

        this.yAxisGroup = this.g.append('g')
            .attr('class', 'y-axis');

        // Create path for line
        this.path = this.g.append('path')
            .attr('class', 'line')
            .attr('fill', 'none')
            .attr('stroke', this.options.strokeColor)
            .attr('stroke-width', this.options.strokeWidth);

        // Create group for points
        this.pointsGroup = this.g.append('g').attr('class', 'points');
    }

    // Main plotting function
    plot(xOrY, y = null) {
        // Parse input data
        if (y === null) {
            // Only y values provided, generate x as indices
            this.data = xOrY.map((yVal, i) => ({ x: i, y: yVal }));
        } else {
            // Both x and y provided
            this.data = xOrY.map((xVal, i) => ({ x: xVal, y: y[i] }));
        }

        this.updatePlot();
    }

    // Add single data point
    addData(xOrY, y = null) {
        let newPoint;

        if (y === null) {
            // Only y value provided
            const nextX = this.data.length > 0 ? this.data[this.data.length - 1].x + 1 : 0;
            newPoint = { x: nextX, y: xOrY };
        } else {
            // Both x and y provided
            newPoint = { x: xOrY, y: y };
        }

        this.data.push(newPoint);
        this.updatePlot();
    }

    // Add multiple data points
    addDataPoints(xOrY, y = null) {
        if (y === null) {
            // Only y values provided
            const startX = this.data.length > 0 ? this.data[this.data.length - 1].x + 1 : 0;
            const newPoints = xOrY.map((yVal, i) => ({ x: startX + i, y: yVal }));
            this.data.push(...newPoints);
        } else {
            // Both x and y provided
            const newPoints = xOrY.map((xVal, i) => ({ x: xVal, y: y[i] }));
            this.data.push(...newPoints);
        }

        this.updatePlot();
    }

    // Clear all data
    clear() {
        this.data = [];
        this.updatePlot();
    }

    // Update the plot
    updatePlot() {
        if (this.data.length === 0) {
            this.path.attr('d', '');
            this.pointsGroup.selectAll('.point').remove();
            return;
        }

        // Uniformize the distribution of number of points per x-axis bin
        if (this.data.length > 2000) {
            this.binifyData(1000)
        }

        // Update scales
        const xExtent = d3.extent(this.data, d => d.x);
        const yExtent = d3.extent(this.data, d => d.y);

        // Add some padding to y scale
        const yPadding = (yExtent[1] - yExtent[0]) * 0.1;

        this.xScale.domain(xExtent);
        this.yScale.domain([yExtent[0] - yPadding, yExtent[1] + yPadding]);

        // Update axes
        const xAxis = d3.axisBottom(this.xScale);
        const yAxis = d3.axisLeft(this.yScale);

        this.xAxisGroup
            .transition()
            .duration(this.options.animationDuration)
            .call(xAxis);

        this.yAxisGroup
            .transition()
            .duration(this.options.animationDuration)
            .call(yAxis);

        // Update line
        this.path
            .datum(this.data)
            .transition()
            .duration(this.options.animationDuration)
            .attr('d', this.line);

        // Update points
        if (this.options.showPoints) {
            const points = this.pointsGroup.selectAll('.point')
                .data(this.data);

            // Remove old points
            points.exit()
                .transition()
                .duration(this.options.animationDuration)
                .attr('r', 0)
                .remove();

            // Add new points
            const newPoints = points.enter()
                .append('circle')
                .attr('class', 'point')
                .attr('cx', d => this.xScale(d.x))
                .attr('cy', d => this.yScale(d.y))
                .attr('r', 0)
                .attr('fill', this.options.strokeColor);

            // Update all points
            points.merge(newPoints)
                .transition()
                .duration(this.options.animationDuration)
                .attr('cx', d => this.xScale(d.x))
                .attr('cy', d => this.yScale(d.y))
                .attr('r', this.options.pointRadius);
        }
    }

    // Uniformize the distribution of number of points per x-axis bin
    binifyData(n) {
        let minNumber = this.data[0].x
        let maxNumber = this.data[0].x
        for (let i = 0; i < this.data.length; i++) {
            if (this.data[i].x < minNumber) {
                minNumber = this.data[i].x
            }
            if (this.data[i].x > maxNumber) {
                maxNumber = this.data[i].x
            }
        }
        const binSize = (maxNumber - minNumber) / n

        let bins = []
        let bin = []
        let currentBinStart = minNumber
        for (let i = 0; i < this.data.length; i++) {
            if (this.data[i].x > currentBinStart + binSize) {
                bins.push(bin)
                bin = [this.data[i]]
                currentBinStart = this.data[i].x
            } else {
                bin.push(this.data[i])
            }
        }

        if (bin.length > 0) {
            bins.push(bin)
        }

        this.data = []
        for (let i = 0; i < bins.length; i++) {
            let avgX = 0
            let avgY = 0
            for (let j = 0; j < bins[i].length; j++) {
                avgX += bins[i][j].x
                avgY += bins[i][j].y
            }
            avgX /= bins[i].length
            avgY /= bins[i].length
            this.data.push({ x: avgX, y: avgY })
        }
    }

    // Update styling options
    updateOptions(newOptions) {
        this.options = { ...this.options, ...newOptions };

        // Update visual elements
        this.path
            .attr('stroke', this.options.strokeColor)
            .attr('stroke-width', this.options.strokeWidth);

        this.pointsGroup.selectAll('.point')
            .attr('fill', this.options.strokeColor)
            .attr('r', this.options.showPoints ? this.options.pointRadius : 0);
    }

    // Get current data
    getData() {
        return [...this.data];
    }

    // Auto-resize to container (call this if container size changes)
    autoResize() {
        const containerNode = this.container.node();
        const containerRect = containerNode.getBoundingClientRect();
        const containerWidth = containerRect.width || containerNode.offsetWidth;
        const containerHeight = containerRect.height || containerNode.offsetHeight;

        if (containerWidth > 0 && containerHeight > 0) {
            this.resize(containerWidth, containerHeight);
        }

        this.options.width = width;
        this.options.height = height;
        this.width = width - this.options.margin.left - this.options.margin.right;
        this.height = height - this.options.margin.top - this.options.margin.bottom;

        // Update SVG dimensions
        this.svg
            .attr('width', this.options.width)
            .attr('height', this.options.height);

        // Update scales range
        this.xScale.range([0, this.width]);
        this.yScale.range([this.height, 0]);

        // Update axis position
        this.xAxisGroup.attr('transform', `translate(0, ${this.height})`);

        // Redraw
        this.updatePlot();
    }
}

// Export for different module systems
if (typeof module !== 'undefined' && module.exports) {
    module.exports = SimplePlot;
} else if (typeof define === 'function' && define.amd) {
    define([], function () { return SimplePlot; });
} else {
    window.SimplePlot = SimplePlot;
}