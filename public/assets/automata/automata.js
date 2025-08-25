resize_canvas(1500, 800)

const rule_slider = document.getElementById("rule")

const size = 5
const height = HEIGHT / size
const width = WIDTH / size
const grid = Array.from(Array(height), () => Array(width).fill(0))
let rule = 30

hsl = (h, s, l) => `hsl(${h}, ${s}%, ${l}%)`

draw_grid = () => {
    for (var i = 0; i < height; i++) {
        for (var j = 0; j < width; j++) {
            if (grid[i][j] != 0) {
                draw_rectangle(j * size, i * size, size, size, 'white')
            }
        }
    }
}

map_config = (rule, left, current, right) => {
    const a = left == 0 ? '0' : '1'
    const b = current == 0 ? '0' : '1'
    const c = right == 0 ? '0' : '1'
    const key = parseInt(a + b + c, 2)
    let mapping = rule.toString(2).padStart(8, '0')
    return parseInt(mapping[7 - key])
}

update_grid = () => {
    for (var i = 0; i < height; i++) {
        for (var j = 0; j < width; j++) {
            grid[i][j] = 0
        }
    }

    grid[0][Math.floor(width / 2)] = 1
    for (var i = 1; i < height; i++) {
        for (var j = 0; j < width; j++) {
            const p = j - 1 == -1 ? width - 1 : j - 1
            const left = grid[i - 1][p % width]
            const right = grid[i - 1][(j + 1) % width]
            const current = grid[i - 1][j]
            grid[i][j] = map_config(rule, left, current, right)
        }
    }
}

rule_slider.oninput = () => {
    rule = parseInt(rule_slider.value)
    update_grid()
    clear_canvas()
    draw_grid()
}

update_grid()
clear_canvas()
draw_grid()