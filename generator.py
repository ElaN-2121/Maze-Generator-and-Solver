import random
def generate_maze(maze):
    rows = maze.rows
    cols = maze.cols
    
    stack = []
    start_row = 0
    start_col = 0

    current = maze.grid[start_row][start_col]
    current.visited = True

    stack.append(current)

    while stack:

        current = stack[-1]
        neighbors = get_unvisited_neighbors(maze, current)

        if neighbors:
            direction, next_cell = random.choice(neighbors)
            remove_walls(current, next_cell, direction)
            next_cell.visited = True

            stack.append(next_cell)

        else:
            stack.pop()


def get_unvisited_neighbors(maze, cell):

    neighbors = []
    row = cell.row
    col = cell.col

    directions = [
        ("top", row - 1, col),
        ("right", row, col + 1),
        ("bottom", row + 1, col),
        ("left", row, col - 1)
    ]

    for direction, r, c in directions:

        if 0 <= r < maze.rows and 0 <= c < maze.cols:

            neighbor = maze.grid[r][c]

            if not neighbor.visited:
                neighbors.append((direction, neighbor))

    return neighbors


def remove_walls(current, next_cell, direction):

    if direction == "top":
        current.walls["top"] = False
        next_cell.walls["bottom"] = False

    elif direction == "right":
        current.walls["right"] = False
        next_cell.walls["left"] = False

    elif direction == "bottom":
        current.walls["bottom"] = False
        next_cell.walls["top"] = False

    elif direction == "left":
        current.walls["left"] = False
        next_cell.walls["right"] = False