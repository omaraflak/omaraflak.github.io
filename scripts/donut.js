const create_donut = (donut_radius, ring_radius) => {
    const circle = create_matrix_by_columns(60, (i) => {
        const theta = 2 * Math.PI * i / 60
        return [
            ring_radius * Math.cos(theta) + donut_radius,
            ring_radius * Math.sin(theta),
            0
        ]
    })

    let donut = [[], [], []]
    for (var i = 0; i < 150; i++) {
        const theta = 2 * Math.PI * i / 150
        donut = matrix_concat_columns(donut, matrix_rotate_y(circle, theta))
    }

    return matrix_add_columns(donut, CENTER3)
}

const rotation = rotation_matrix_xyz(Math.PI / 200, Math.PI / 100, Math.PI / 60)

let donut = create_donut(100, 60)

const update = () => {
    clear_canvas()
    for (let p of columnsOf(donut)) {
        draw_rectangle(p[0], p[1], 1, 1, "white")
    }
    donut = matrix_add_columns(matrix_dot(rotation, matrix_sub_columns(donut, CENTER3)), CENTER3)
    requestAnimationFrame(update)
}

update()