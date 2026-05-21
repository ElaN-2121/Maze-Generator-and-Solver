# main.py
import pygame
import random
import sys
from maze import Maze
import generator
import solver
from visualizer import MazeVisualizer, WHITE, BLACK, RED, BLUE, GREEN

# Constants
ROWS, COLS = 12, 16
CELL_SIZE, MARGIN = 30, 40
WIDTH = COLS * CELL_SIZE + 2 * MARGIN
HEIGHT = ROWS * CELL_SIZE + 2 * MARGIN


# ============================================================
# CELL CLASS (for generator.py compatibility)
# ============================================================
class Cell:
    """Cell object that generator.py expects."""
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.visited = False
        self.walls = {"top": True, "right": True, "bottom": True, "left": True}


# ============================================================
# MAZE ADAPTER - wraps Maze to work with generator.py
# ============================================================
class MazeAdapter:
    """
    Wraps the Maze class to provide the .grid interface that generator.py expects.
    generator.py accesses grid as: maze.grid[row][col] (0-indexed 2D list)
    Synchronizes cell walls to/from Maze's north_wall/east_wall arrays (1-indexed).
    
    Wall mapping:
      - north_wall[r][c] = top wall of cell (r,c) where r,c are 1-indexed
      - east_wall[r][c]  = right wall of cell (r,c)
      - South wall of (r,c) = north_wall[r+1][c]
      - West wall of (r,c)  = east_wall[r][c-1]
    """
    def __init__(self, maze):
        self.maze = maze
        self.rows = maze.rows
        self.cols = maze.cols
        # Build 0-indexed 2D list for generator.py compatibility
        # grid[0][0] = top-left cell, grid[rows-1][cols-1] = bottom-right cell
        self.grid = []
        for r in range(self.rows):
            row_cells = []
            for c in range(self.cols):
                row_cells.append(Cell(r, c))
            self.grid.append(row_cells)
        self._sync_from_maze()

    def _sync_from_maze(self):
        """Copy Maze's wall state (1-indexed) into Cell objects (0-indexed)."""
        for r in range(self.rows):
            for c in range(self.cols):
                maze_r = r + 1  # Convert to 1-indexed for Maze
                maze_c = c + 1
                cell = self.grid[r][c]
                cell.walls["top"] = (self.maze.north_wall[maze_r][maze_c] == 1)
                cell.walls["right"] = (self.maze.east_wall[maze_r][maze_c] == 1)
                # bottom wall = north_wall of cell below
                if maze_r < self.maze.rows:
                    cell.walls["bottom"] = (self.maze.north_wall[maze_r + 1][maze_c] == 1)
                else:
                    cell.walls["bottom"] = True  # outer boundary
                # left wall = east_wall of cell to the left
                if maze_c > 1:
                    cell.walls["left"] = (self.maze.east_wall[maze_r][maze_c - 1] == 1)
                else:
                    cell.walls["left"] = True  # outer boundary

    def sync_to_maze(self):
        """Copy Cell wall state (0-indexed) back into Maze's arrays (1-indexed)."""
        for r in range(self.rows):
            for c in range(self.cols):
                maze_r = r + 1
                maze_c = c + 1
                cell = self.grid[r][c]
                self.maze.north_wall[maze_r][maze_c] = 1 if cell.walls["top"] else 0
                self.maze.east_wall[maze_r][maze_c] = 1 if cell.walls["right"] else 0


# ============================================================
# MODIFIED GENERATOR - uses generator.py logic with visualization
# ============================================================
def generate_with_viz(maze_adapter, visualizer, screen, clock):
    """
    Generate maze using generator.py's algorithm, with step-by-step visualization.
    generator.py uses 0-indexed cells; visualizer uses 1-indexed Maze coordinates.
    """
    import random as rand

    grid = maze_adapter.grid
    stack = []

    # Start at (0,0) in 0-indexed grid
    current = grid[0][0]
    current.visited = True
    stack.append(current)

    while stack:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        current = stack[-1]
        neighbors = generator.get_unvisited_neighbors(maze_adapter, current)

        if neighbors:
            direction, next_cell = rand.choice(neighbors)
            generator.remove_walls(current, next_cell, direction)
            next_cell.visited = True
            stack.append(next_cell)

            # Sync walls back to Maze
            maze_adapter.sync_to_maze()

            # Visualize (convert 0-indexed cell coords to 1-indexed maze coords)
            viz_r = next_cell.row + 1
            viz_c = next_cell.col + 1
            visualizer.animate_generation(maze_adapter.maze, (viz_r, viz_c))
            clock.tick(120)
        else:
            stack.pop()
            # Visualize backtracking
            if stack:
                current = stack[-1]
                viz_r = current.row + 1
                viz_c = current.col + 1
                visualizer.animate_generation(maze_adapter.maze, (viz_r, viz_c))
                clock.tick(120)


# ============================================================
# CONVERT MAZE TO 0/1 MATRIX (for solver.py)
# ============================================================
def maze_to_matrix(maze):
    """
    Convert Maze's wall representation to a 2D 0/1 grid.
    Each cell becomes 2x2 in the matrix:
      - Cell center = 0 (open)
      - Walls between cells = 1 (wall) or 0 (open)
    Matrix size: (2*rows+1) x (2*cols+1)
    """
    matrix_rows = 2 * maze.rows + 1
    matrix_cols = 2 * maze.cols + 1
    matrix = [[1] * matrix_cols for _ in range(matrix_rows)]

    for r in range(1, maze.rows + 1):
        for c in range(1, maze.cols + 1):
            mr, mc = 2 * r - 1, 2 * c - 1
            matrix[mr][mc] = 0  # cell center is always open

            # East opening -> open cell to the right
            if maze.east_wall[r][c] == 0:
                matrix[mr][mc + 1] = 0

            # South opening -> open cell below (north wall of cell below)
            if r < maze.rows and maze.north_wall[r + 1][c] == 0:
                matrix[mr + 1][mc] = 0

    # Open entry and exit on the outer boundary
    # Entry: left wall of (start_r, start_c) = east_wall[start_r][0]
    for r in range(1, maze.rows + 1):
        if maze.east_wall[r][0] == 0:
            matrix[2 * r - 1][0] = 0
    # Exit: right wall of (end_r, end_c) = east_wall[end_r][COLS]
    for r in range(1, maze.rows + 1):
        if hasattr(maze, 'east_wall') and len(maze.east_wall[r]) > maze.cols:
            if maze.east_wall[r][maze.cols] == 0:
                matrix[2 * r - 1][-1] = 0
        else:
            # east_wall array has COLS+1 columns (0..COLS)
            if maze.east_wall[r][maze.cols] == 0:
                matrix[2 * r - 1][-1] = 0

    return matrix


def maze_cell_to_matrix(r, c):
    """Convert 1-indexed maze coordinates to matrix coordinates."""
    return (2 * r - 1, 2 * c - 1)


def matrix_to_maze_cell(mr, mc):
    """Convert matrix coordinates to 1-indexed maze coordinates."""
    return ((mr + 1) // 2, (mc + 1) // 2)


# ============================================================
# MODIFIED SOLVER - uses solver.py with visualization
# ============================================================
def solve_with_viz(maze, visualizer, screen, clock, start_cell, end_cell):
    """
    Solve maze using DFS backtracking with step-by-step visualization.
    """
    # Convert maze to 0/1 matrix
    matrix = maze_to_matrix(maze)
    start = maze_cell_to_matrix(start_cell[0], start_cell[1])
    end = maze_cell_to_matrix(end_cell[0], end_cell[1])

    visited = set()
    current_path = []
    dead_ends = []

    def is_safe_to_step(row, col):
        if row < 0 or row >= len(matrix):
            return False
        if col < 0 or col >= len(matrix[0]):
            return False
        if matrix[row][col] == 1:
            return False
        if (row, col) in visited:
            return False
        return True

    def explore(row, col):
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        visited.add((row, col))
        current_path.append((row, col))

        # Convert to maze coordinates for visualization
        maze_cell = matrix_to_maze_cell(row, col)
        path_maze = [matrix_to_maze_cell(r, c) for r, c in current_path]
        dead_maze = [matrix_to_maze_cell(r, c) for r, c in dead_ends]

        visualizer.animate_solver(maze, maze_cell, path_maze, dead_maze)
        clock.tick(60)

        if (row, col) == end:
            return True

        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        # Randomize directions for more interesting visualization
        random.shuffle(directions)

        for move_row, move_col in directions:
            next_row = row + move_row
            next_col = col + move_col

            if is_safe_to_step(next_row, next_col):
                if explore(next_row, next_col):
                    return True

        dead_ends.append((row, col))
        current_path.pop()

        # Visualize backtracking
        if current_path:
            maze_cell = matrix_to_maze_cell(
                current_path[-1][0], current_path[-1][1]
            )
        else:
            maze_cell = matrix_to_maze_cell(row, col)
        path_maze = [matrix_to_maze_cell(r, c) for r, c in current_path]
        dead_maze = [matrix_to_maze_cell(r, c) for r, c in dead_ends]
        visualizer.animate_solver(maze, maze_cell, path_maze, dead_maze)
        clock.tick(60)

        return False

    found = explore(start[0], start[1])

    path_maze = [matrix_to_maze_cell(r, c) for r, c in current_path]
    dead_maze = [matrix_to_maze_cell(r, c) for r, c in dead_ends]

    return path_maze, dead_maze, found


# ============================================================
# ADD VISUALIZER-COMPATIBLE ATTRIBUTES TO MAZE
# ============================================================
def prepare_maze_for_viz(maze):
    """Add the attribute names that visualizer.py expects."""
    maze.northWall = maze.north_wall
    maze.eastWall = maze.east_wall
    maze.ROWS = maze.rows
    maze.COLS = maze.cols


# ============================================================
# MAIN APPLICATION
# ============================================================
class MazeApp:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Maze Generator & Solver")
        self.clock = pygame.time.Clock()
        self.maze = Maze(ROWS, COLS)
        self.visualizer = MazeVisualizer(self.screen, CELL_SIZE)

    def run(self):
        # Prepare maze for visualization
        prepare_maze_for_viz(self.maze)

        # Create adapter for generator
        adapter = MazeAdapter(self.maze)

        # Set start and end points
        self.start_r, self.start_c = 1, 1
        self.end_r, self.end_c = ROWS, COLS

        # Open entry and exit walls on the outer boundary
        self.maze.east_wall[self.start_r][0] = 0  # Open left wall of start cell
        self.maze.east_wall[self.end_r][COLS] = 0  # Open right wall of end cell

        # Phase 1: Generate Maze
        print("Generating maze...")
        generate_with_viz(adapter, self.visualizer, self.screen, self.clock)

        # Pause after generation
        self.maze.start = (self.start_r, self.start_c)
        self.maze.end = (self.end_r, self.end_c)
        prepare_maze_for_viz(self.maze)
        self.visualizer.draw_maze(self.maze)
        
        # Draw start and end markers
        self._draw_marker(self.start_r, self.start_c, GREEN)
        self._draw_marker(self.end_r, self.end_c, (255, 215, 0))  # Gold
        pygame.display.flip()
        
        print("Maze generated! Press any key to solve...")
        self._wait_for_key()

        # Phase 2: Solve Maze
        print("Solving maze...")
        path, dead_ends, found = solve_with_viz(
            self.maze, self.visualizer, self.screen, self.clock,
            (self.start_r, self.start_c),
            (self.end_r, self.end_c)
        )

        if found:
            print(f"Path found! Length: {len(path)}")
            pygame.display.set_caption("Maze Solved! Press any key to exit...")
        else:
            print("No path found!")
            pygame.display.set_caption("No path found! Press any key to exit...")

        # Final display
        prepare_maze_for_viz(self.maze)
        self.visualizer.animate_solver(
            self.maze,
            (self.end_r, self.end_c),
            path,
            dead_ends
        )
        
        # Draw start and end markers on final display
        self._draw_marker(self.start_r, self.start_c, GREEN)
        self._draw_marker(self.end_r, self.end_c, (255, 215, 0))  # Gold
        pygame.display.flip()

        # Wait for user to exit
        self._wait_for_key()
        pygame.quit()
        sys.exit()

    def _draw_marker(self, r, c, color):
        """Draw a circular marker at the given cell."""
        x = (c - 1) * CELL_SIZE + MARGIN + CELL_SIZE // 2
        y = (r - 1) * CELL_SIZE + MARGIN + CELL_SIZE // 2
        pygame.draw.circle(self.screen, color, (int(x), int(y)), CELL_SIZE // 3)

    def _wait_for_key(self):
        """Wait until user presses a key or closes window."""
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    waiting = False
            self.clock.tick(30)


if __name__ == "__main__":
    MazeApp().run()