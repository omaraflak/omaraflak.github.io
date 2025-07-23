let WIDTH = 500
let HEIGHT = 500

const canvas = document.getElementById("canvas")
const ctx = canvas.getContext("2d")

canvas.height = HEIGHT
canvas.width = WIDTH

let CENTER = [WIDTH / 2, HEIGHT / 2]
let CENTER3 = [...CENTER, 0]

const resize_canvas = (width, height) => {
    HEIGHT = height
    WIDTH = width
    CENTER = [width / 2, height / 2]
    CENTER3 = [...CENTER, 0]
    canvas.height = height
    canvas.width = width
}

const draw_rectangle = (x, y, w, h, color) => {
    ctx.fillStyle = color
    ctx.fillRect(x, y, w, h)
}

const draw_line = (sx, sy, ex, ey, color) => {
    ctx.strokeStyle = color
    ctx.beginPath()
    ctx.moveTo(sx, sy)
    ctx.lineTo(ex, ey)
    ctx.stroke()
}

const draw_circle = (x, y, radius, color) => {
    ctx.beginPath();
    ctx.arc(x, y, radius, 0, 2 * Math.PI, false)
    ctx.lineWidth = 2
    ctx.strokeStyle = color
    ctx.stroke();
}

const random_int = (max) => Math.floor(max * Math.random())

const rgba = (r, g, b, a = 1) => `rgba(${r}, ${g}, ${b}, ${a})`

const random_rgba = (alpha = Math.random()) => rgba(random_int(255), random_int(255), random_int(255), alpha)

const clear_canvas = (color = "black") => draw_rectangle(0, 0, WIDTH, HEIGHT, color)