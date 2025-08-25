const magnitude = (x, y) => Math.sqrt(x * x + y * y)

create_particles = (total) => Array.from(Array(total), create_particle)

create_particle = () => {
    return {
        "x": Math.random() * WIDTH,
        "y": Math.random() * HEIGHT,
        "vx": Math.random() - 0.5,
        "vy": Math.random() - 0.5,
        "size": 3,
        "color": random_rgba(1)
    }
}

update_particle = (p, particles, min_distance) => {
    const copy = Object.assign({}, p)

    let ax = 0
    let ay = 0

    for (const other of particles) {
        if (other == p) {
            continue;
        }

        const dx = other.x - copy.x
        const dy = other.y - copy.y
        const d = dx * dx + dy * dy
        const g = Math.sqrt(d) < min_distance ? -1 : 1

        ax += g * dx / d
        ay += g * dy / d
    }

    const a = magnitude(ax, ay)
    if (a > 0.2) {
        ax *= 0.2 / a
        ay *= 0.2 / a
    }

    copy.vx += ax
    copy.vy += ay

    const v = magnitude(copy.vx, copy.vy)
    if (v > 4) {
        copy.vx *= 4 / v
        copy.vy *= 4 / v
    }

    copy.x += copy.vx
    copy.y += copy.vy

    if (copy.x <= 0 || copy.x + copy.size >= WIDTH) {
        copy.vx *= -1
    }
    if (copy.y <= 0 || copy.y + copy.size >= HEIGHT) {
        copy.vy *= -1
    }

    return copy
}

draw_particle = (p) => draw_rectangle(p.x, p.y, p.size, p.size, p.color)

const total_particles_slider = document.getElementById("total_particles")
const total_particles_placeholder = document.getElementById("total_particles_placeholder")

const min_distance_slider = document.getElementById("min_distance")
const min_distance_placeholder = document.getElementById("min_distance_placeholder")

min_distance_slider.oninput = function () {
    min_distance = parseInt(this.value);
    min_distance_placeholder.innerText = min_distance
}

total_particles_slider.oninput = function () {
    total_particles = parseInt(this.value);
    total_particles_placeholder.innerText = total_particles
    should_recreate_particles = true
}

let min_distance = 50
let total_particles = 500
let should_recreate_particles = false
let particles = create_particles(total_particles)

const update = () => {
    clear_canvas()

    particles = particles.map(p => update_particle(p, particles, min_distance))
    particles.forEach(draw_particle)

    if (should_recreate_particles) {
        should_recreate_particles = false
        particles = create_particles(total_particles)
    }

    requestAnimationFrame(update)
}

update()