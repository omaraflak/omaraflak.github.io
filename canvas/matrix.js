const create_matrix = (height, width, init) => Array.from(Array(height), (_, i) => Array.from(Array(width), (_, j) => init(i, j)))

const create_matrix_by_rows = (height, init) => Array.from(Array(height), (_, i) => init(i))

const create_matrix_by_columns = (width, init) => transpose(create_matrix_by_rows(width, init))

const create_row_matrix = (values) => create_matrix(1, values.length, (i, j) => values[j])

const create_column_matrix = (values) => create_matrix(values.length, 1, (i, j) => values[i])

const rows = (matrix) => matrix.length

const columns = (matrix) => matrix[0].length

const zeros = () => 0

const matrix_row = (matrix, i) => matrix[i]

const matrix_column = (matrix, j) => matrix.map((_, i) => matrix[i][j])

const copy_matrix = (matrix) => create_matrix(rows(matrix), columns(matrix), (i, j) => matrix[i][j])

const transpose = (matrix) => create_matrix(columns(matrix), rows(matrix), (i, j) => matrix[j][i])

const matrix_add = (matrix1, matrix2) => create_matrix(rows(matrix1), columns(matrix1), (i, j) => matrix1[i][j] + matrix2[i][j])

const matrix_add_rows = (matrix, values) => create_matrix(rows(matrix), columns(matrix), (i, j) => matrix[i][j] + values[j])

const matrix_add_columns = (matrix, values) => create_matrix(rows(matrix), columns(matrix), (i, j) => matrix[i][j] + values[i])

const matrix_sub = (matrix1, matrix2) => create_matrix(rows(matrix1), columns(matrix1), (i, j) => matrix1[i][j] - matrix2[i][j])

const matrix_sub_rows = (matrix, values) => create_matrix(rows(matrix), columns(matrix), (i, j) => matrix[i][j] - values[j])

const matrix_sub_columns = (matrix, values) => create_matrix(rows(matrix), columns(matrix), (i, j) => matrix[i][j] - values[i])

const matrix_mul = (matrix, value) => create_matrix(rows(matrix), columns(matrix), (i, j) => matrix[i][j] * value)

const matrix_apply = (matrix, fun) => create_matrix(rows(matrix), columns(matrix), (i, j) => fun(matrix[i][j]))

const matrix_apply_rows = (matrix, fun) => create_matrix_by_rows(rows(matrix), (i) => fun(matrix_row(matrix, i)))

const matrix_apply_columns = (matrix, fun) => create_matrix_by_columns(columns(matrix), (j) => fun(matrix_column(matrix, j)))

const matrix_concat_rows = (matrix1, matrix2) => create_matrix(rows(matrix1) + rows(matrix2), columns(matrix1), (i, j) => i < rows(matrix1) ? matrix1[i][j] : matrix2[i - rows(matrix1)][j])

const matrix_concat_columns = (matrix1, matrix2) => create_matrix(rows(matrix1), columns(matrix1) + columns(matrix2), (i, j) => j < columns(matrix1) ? matrix1[i][j] : matrix2[i][j - columns(matrix1)])

const matrix_push_row = (matrix, row) => matrix.push(row)

const matrix_push_column = (matrix, column) => column.forEach((x, i) => matrix[i].push(x))

const matrix_dot = (matrix1, matrix2) => {
    const height = rows(matrix1)
    const width = columns(matrix2)
    const output = create_matrix(height, width, zeros)
    for (var i = 0; i < height; i++) {
        for (var j = 0; j < width; j++) {
            let tmp = 0
            for (var k = 0; k < matrix2.length; k++) {
                tmp += matrix1[i][k] * matrix2[k][j]
            }
            output[i][j] = tmp
        }
    }
    return output
}

const rotation_matrix_x = (rad) => {
    const cos = Math.cos(rad)
    const sin = Math.sin(rad)
    return [
        [1, 0, 0],
        [0, cos, -sin],
        [0, sin, cos]
    ]
}

const rotation_matrix_y = (rad) => {
    const cos = Math.cos(rad)
    const sin = Math.sin(rad)
    return [
        [cos, 0, sin],
        [0, 1, 0],
        [-sin, 0, cos]
    ]
}

const rotation_matrix_z = (rad) => {
    const cos = Math.cos(rad)
    const sin = Math.sin(rad)
    return [
        [cos, -sin, 0],
        [sin, cos, 0],
        [0, 0, 1]
    ]
}

const rotation_matrix_xyz = (rad_x, rad_y, rad_z) => matrix_dot(rotation_matrix_z(rad_x), matrix_dot(rotation_matrix_y(rad_y), rotation_matrix_x(rad_z)))

const matrix_rotate_x = (matrix, rad) => matrix_dot(rotation_matrix_x(rad), matrix)

const matrix_rotate_y = (matrix, rad) => matrix_dot(rotation_matrix_y(rad), matrix)

const matrix_rotate_z = (matrix, rad) => matrix_dot(rotation_matrix_z(rad), matrix)

function* rowsOf(matrix) {
    for (let i = 0; i < rows(matrix); i++) {
        yield matrix_row(matrix, i);
    }
}

function* columnsOf(matrix) {
    for (let j = 0; j < columns(matrix); j++) {
        yield matrix_column(matrix, j);
    }
}