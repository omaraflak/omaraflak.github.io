class Brain {
    constructor() {
        const r = () => Math.random() - 0.5
        this.weights = create_matrix(4, 4, r)
    }

    process(x, y) {
        // distance ratio to each wall: top, right, bottom, left
        const inputs = [
            [
                y / HEIGHT,
                (WIDTH - x) / WIDTH,
                (HEIGHT - y) / HEIGHT,
                x / WIDTH
            ]
        ]

        // mini neural network
        const output = matrix_apply(matrix_dot(inputs, this.weights), Math.tanh)

        return {
            'dx': output[0][0] - output[0][1],
            'dy': output[0][2] - output[0][3]
        }
    }

    static merge(brain1, brain2) {
        const child = new Brain()

        // inheritance
        child.weights[0] = brain1.weights[0]
        child.weights[1] = brain1.weights[1]
        child.weights[2] = brain2.weights[2]
        child.weights[3] = brain2.weights[3]

        // mutation
        if (Math.random() < 0.05) {
            child.weights[0][0] = Math.random() - 0.5
            child.weights[2][0] = Math.random() - 0.5
        }
        return child
    }
}

class Particle {
    constructor(x, y, size, color) {
        this.x = x
        this.y = y
        this.size = size
        this.color = color
        this.brain = new Brain()
    }

    draw() {
        draw_rectangle(this.x, this.y, this.size, this.size, this.color)
    }

    update() {
        const { dx, dy } = this.brain.process(this.x, this.y)
        this.x += 3 * dx
        this.y += 3 * dy

        if (this.x < 0) {
            this.x = 0
        }
        if (this.x > WIDTH - this.size) {
            this.x = WIDTH - this.size
        }
        if (this.y < 0) {
            this.y = 0
        }
        if (this.y > HEIGHT - this.size) {
            this.y = HEIGHT - this.size
        }
    }
}

const filter_survivors = (particles) => {
    return particles.filter(should_survive)
        .map(value => ({ value, sort: Math.random() }))
        .sort((a, b) => a.sort - b.sort)
        .map(({ value }) => value)
}

const reproduce_particles = (particles, max_population) => {
    const new_generation = []
    for (var i = 0; i < particles.length - particles.length % 2; i += 2) {
        const child = new_particle()
        child.brain = Brain.merge(particles[i].brain, particles[i + 1].brain)

        const parent1 = new_particle()
        parent1.brain = particles[i].brain

        const parent2 = new_particle()
        parent2.brain = particles[i + 1].brain

        new_generation.push(parent1)
        new_generation.push(parent2)
        new_generation.push(child)

        if (max_population > 0 && new_generation.length > max_population) {
            break
        }
    }
    return new_generation
}

const population_size_plot = document.getElementById("population_size")
Plotly.newPlot(population_size_plot, [{ y: [], type: "scatter" }], { title: "Population size" })

const survival_ratio_plot = document.getElementById("survival_ratio")
Plotly.newPlot(survival_ratio_plot, [{ y: [], type: "scatter" }], { title: "Survival ratio" })

const statusText = document.getElementById("status")

// CONTROLS NEW PARTICLE CREATION
const new_particle = () => new Particle((WIDTH / 2) * Math.random(), HEIGHT * Math.random(), 3, "yellow")

// SURVIVAL PREDICATE
const should_survive = (particle) => {
    return particle.x > WIDTH / 2
}

// CONTROLS
const fast_forward_epochs = 0
const initial_population = 100
const iterations_per_epoch = 200
const total_epochs = 15
const max_population_size = 15000

const population_size = [initial_population]
const survival_ratio = []

let particles = Array.from(Array(initial_population), new_particle)
let current_iteration = 1
let current_epoch = 0

const update = () => {
    const should_draw = current_epoch >= fast_forward_epochs
    statusText.innerText = `${current_epoch}/${total_epochs}`

    if (should_draw) {
        clear_canvas()
    }

    draw_line(WIDTH / 2, 0, WIDTH / 2, HEIGHT, "red")

    for (let p of particles) {
        p.update()
        if (should_draw) {
            p.draw()
        }
    }

    if (current_iteration % iterations_per_epoch == 0) {
        const sizeBefore = particles.length
        particles = filter_survivors(particles)
        survival_ratio.push(particles.length / sizeBefore)
        Plotly.update(survival_ratio_plot, { y: [survival_ratio] })

        particles = reproduce_particles(particles, max_population_size)
        population_size.push(particles.length)
        Plotly.update(population_size_plot, { y: [population_size] })

        current_epoch++
        if (current_epoch - 1 == total_epochs) {
            return
        }
    }

    current_iteration++
    if (should_draw) {
        requestAnimationFrame(update)
    }
}

for (var i = 0; i <= fast_forward_epochs * iterations_per_epoch; i++) {
    update()
}