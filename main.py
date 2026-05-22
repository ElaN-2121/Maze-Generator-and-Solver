import pygame
import random
import sys

from maze import Maze
import generator
import solver
from visualizer import MazeVisualizer, WHITE, GREEN


ROWS, COLS = 12, 16
CELL_SIZE, MARGIN = 30, 40
WIDTH = COLS * CELL_SIZE + 2 * MARGIN
HEIGHT = ROWS * CELL_SIZE + 2 * MARGIN



class Cell:
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.visited = False
        self.walls = {"top": True, "right": True, "bottom": True, "left": True}



class MazeAdapter:
    def __init__(self, maze):
        self.maze = maze
        self.rows = maze.rows
        self.cols = maze.cols

        self.grid = [
            [Cell(r, c) for c in range(self.cols)]
            for r in range(self.rows)
        ]

        self._sync_from_maze()

    def _sync_from_maze(self):
        for r in range(self.rows):
            for c in range(self.cols):
                mr, mc = r + 1, c + 1
                cell = self.grid[r][c]

                cell.walls["top"] = self.maze.north_wall[mr][mc] == 1
                cell.walls["right"] = self.maze.east_wall[mr][mc] == 1

                if mr < self.rows:
                    cell.walls["bottom"] = self.maze.north_wall[mr + 1][mc] == 1
                else:
                    cell.walls["bottom"] = True

                if mc > 1:
                    cell.walls["left"] = self.maze.east_wall[mr][mc - 1] == 1
                else:
                    cell.walls["left"] = True

    def sync_to_maze(self):
        for r in range(self.rows):
            for c in range(self.cols):
                mr, mc = r + 1, c + 1
                cell = self.grid[r][c]

                self.maze.north_wall[mr][mc] = 1 if cell.walls["top"] else 0
                self.maze.east_wall[mr][mc] = 1 if cell.walls["right"] else 0



def generate_with_viz(adapter, visualizer, screen, clock):
    stack = []
    start = adapter.grid[0][0]
    start.visited = True
    stack.append(start)

    while stack:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        current = stack[-1]
        neighbors = generator.get_unvisited_neighbors(adapter, current)

        if neighbors:
            direction, nxt = random.choice(neighbors)
            generator.remove_walls(current, nxt, direction)

            nxt.visited = True
            stack.append(nxt)

            adapter.sync_to_maze()

            visualizer.animate_generation(
                adapter.maze,
                (nxt.row + 1, nxt.col + 1)
            )
            clock.tick(120)

        else:
            stack.pop()



class MazeApp:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Maze Generator & Solver")
        self.clock = pygame.time.Clock()

        self.maze = Maze(ROWS, COLS)
        self.visualizer = MazeVisualizer(self.screen, CELL_SIZE)

    def run(self):

        self.screen.fill(WHITE)
        pygame.display.flip()

        self.start_r, self.start_c = 1, 1
        self.end_r, self.end_c = ROWS, COLS

        # ONLY OPEN ENTRY (safe)
        self.maze.north_wall[1][1] = 0

        adapter = MazeAdapter(self.maze)


        print("Generating maze...")
        generate_with_viz(adapter, self.visualizer, self.screen, self.clock)

       
        self.screen.fill(WHITE)

        self.visualizer.draw_maze(
            self.maze,
            start=(1, 1),
            end=(ROWS, COLS)
        )

        self._draw_marker(self.start_r, self.start_c, GREEN)
        self._draw_marker(self.end_r, self.end_c, (255, 215, 0))

        pygame.display.flip()

        print("Maze generated! Press key...")
        self._wait()

     
        print("Solving maze...")

        path, dead, found = solver.solve_maze(self.maze)

        self.screen.fill(WHITE)

        self.visualizer.draw_maze(
            self.maze,
            start=(1, 1),
            end=(ROWS, COLS)
        )

        self.visualizer.animate_solver(
            self.maze,
            (self.end_r, self.end_c),
            path,
            dead
        )

        self._draw_marker(self.start_r, self.start_c, GREEN)
        self._draw_marker(self.end_r, self.end_c, (255, 215, 0))

        pygame.display.flip()

        print("Done. Press key to exit.")
        self._wait()

        pygame.quit()
        sys.exit()


    def _draw_marker(self, r, c, color):
        x = (c - 1) * CELL_SIZE + MARGIN + CELL_SIZE // 2
        y = (r - 1) * CELL_SIZE + MARGIN + CELL_SIZE // 2
        pygame.draw.circle(self.screen, color, (x, y), CELL_SIZE // 3)

    def _wait(self):
        waiting = True
        while waiting:
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if e.type == pygame.KEYDOWN:
                    waiting = False
            self.clock.tick(30)


if __name__ == "__main__":
    MazeApp().run()
