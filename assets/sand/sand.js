resize_canvas(1000, 1000)

const size = 5
const height = HEIGHT / size
const width = WIDTH / size
const grid = Array.from(Array(height), () => Array(width).fill(0))

hsl = (h, s, l) => `hsl(${h}, ${s}%, ${l}%)`

draw_grid = () => {
    for (var i = 0; i < height; i++) {
        for (var j = 0; j < width; j++) {
            if (grid[i][j] == 0) {
                continue
            }
            draw_rectangle(j * size, i * size, size, size, hsl(grid[i][j], 100, 50))
        }
    }
}

update_grid = () => {
    const newGrid = Array.from(Array(height), () => Array(width).fill(0));
    for (var i = 0; i < height; i++) {
        for (var j = 0; j < width; j++) {
            if (grid[i][j] == 0) {
                continue
            }

            if (i + 1 >= height) {
                newGrid[i][j] = grid[i][j]
                continue
            }

            if (grid[i + 1][j] == 0 && newGrid[i + 1][j] == 0) {
                newGrid[i + 1][j] = grid[i][j]
                continue
            }

            dir = Math.random() > 0.5 ? 1 : -1
            if (j + dir >= 0 && j + dir < width && grid[i + 1][j + dir] == 0 && newGrid[i + 1][j + dir] == 0) {
                newGrid[i + 1][j + dir] = grid[i][j]
            } else {
                newGrid[i][j] = grid[i][j]
            }
        }
    }

    for (var i = 0; i < height; i++) {
        for (var j = 0; j < width; j++) {
            grid[i][j] = newGrid[i][j]
        }
    }
}

update = () => {
    clear_canvas()
    draw_grid()
    update_grid()
    requestAnimationFrame(update)
}

let hue = 0
document.onmousemove = (event) => {
    const mouse = map_mouse_with_scale(event.clientX, event.clientY, size)
    const r = mouse.y
    const c = mouse.x
    for (let i = -2; i < 3; i++) {
        for (let j = -2; j < 3; j++) {
            if (0 <= r + i && r + i < height && 0 <= c + j && c + j < width) {
                if (grid[r + i][c + j] == 0) {
                    grid[r + i][c + j] = hue
                }
            }
        }
    }
    hue = (hue + 0.3) % 360
}

update()