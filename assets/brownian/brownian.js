const particles = []
const mean_squared_displacement_plot = new LinePlot('mean_squared_displacement');

const makeParticles = (n) => {
    for (let i = 0; i < n; i++) {
        const particle = { 'x': WIDTH / 2, 'y': HEIGHT / 2, 'history': [] }
        particles.push(particle)
    }
}

const getMeanSquaredDisplacement = () => {
    let msd = 0
    for (var p of particles) {
        msd += Math.pow(p.x - WIDTH / 2, 2) + Math.pow(p.y - HEIGHT / 2, 2)
    }
    msd /= particles.length
    return msd
}

const updateParticles = () => {
    for (var p of particles) {
        const angle = 2 * Math.PI * Math.random()
        const radius = 5
        const dx = radius * Math.cos(angle)
        const dy = radius * Math.sin(angle)
        p.history.push({ 'x': p.x, 'y': p.y })
        if (p.history.length > 10) {
            p.history.shift()
        }
        p.x += dx
        p.y += dy
    }
}

const drawParticles = () => {
    for (var p of particles) {
        draw_rectangle(p.x, p.y, 3, 3, "white")
        for (var i = 0; i < p.history.length - 1; i++) {
            const p1 = p.history[i]
            const p2 = p.history[i + 1]
            draw_line(p1.x, p1.y, p2.x, p2.y, "white")
        }
    }
}

const update = () => {
    clear_canvas()
    updateParticles()
    drawParticles()
    const msd = getMeanSquaredDisplacement()
    mean_squared_displacement_plot.addData(msd);
    requestAnimationFrame(update)
}

resize_canvas(1000, 1000)
makeParticles(100)
update()