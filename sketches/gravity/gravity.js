const magnitude = (x, y) => Math.sqrt(x * x + y * y)

class Particle {
    constructor(x, y, vx, vy) {
        this.x = x
        this.y = y
        this.vx = vx
        this.vy = vy
        this.color = random_rgba()
        this.size = 3
    }

    update(particles, min_distance) {
        let ax = 0
        let ay = 0

        for (const p of particles) {
            if (p == this) {
                continue;
            }

            const dx = p.x - this.x
            const dy = p.y - this.y
            const distance = dx * dx + dy * dy
            let g = Math.sqrt(distance) < min_distance ? -1 : 1

            ax += g * dx / distance
            ay += g * dy / distance
        }

        const l = magnitude(ax, ay)
        if (l > 0.2) {
            ax *= 0.2 / l
            ay *= 0.2 / l
        }
        
        this.vx += ax
        this.vy += ay

        const ll = magnitude(this.vx, this.vy)
        if (ll > 4) {
            this.vx *= 4 / ll
            this.vy *= 4 / ll
        }

        this.x += this.vx
        this.y += this.vy

        if (this.x <= 0 || this.x + this.size >= WIDTH) {
            this.vx *= -1
        }
        if (this.y <= 0 || this.y + this.size >= HEIGHT) {
            this.vy *= -1
        }
    }

    draw() {
        draw_rectangle(this.x, this.y, this.size, this.size, this.color)
    }
}

const create_particles = (total) => Array.from(Array(total), () => new Particle(WIDTH * Math.random(), HEIGHT * Math.random(), 0, 0))

const total_particles_slider = document.getElementById("total_particles")
const total_particles_placeholder = document.getElementById("total_particles_placeholder")

const min_distance_slider = document.getElementById("min_distance")
const min_distance_placeholder = document.getElementById("min_distance_placeholder")

min_distance_slider.oninput = function() {
    min_distance = parseInt(this.value);
    min_distance_placeholder.innerText = min_distance
}

total_particles_slider.oninput = function() {
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
    
    for (const p of particles) {
        p.update(particles, min_distance)
        p.draw()
    }

    if (should_recreate_particles) {
        should_recreate_particles = false
        particles = create_particles(total_particles)
    }

    requestAnimationFrame(update)
}

update()
