import pygame

# Standard Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

class MazeVisualizer:
    def __init__(self, screen, cell_size=25):
        self.screen = screen
        self.cell_size = cell_size

    def draw_maze(self, maze_data):
        """
        maze_data is an object containing northWall, eastWall, ROWS, COLS
        """
        self.screen.fill(WHITE)
        ROWS = len(maze_data.northWall) - 1
        COLS = len(maze_data.eastWall[0]) - 1

        for r in range(1, ROWS + 1):
            for c in range(1, COLS + 1):
                x = (c - 1) * self.cell_size + 20
                y = (r - 1) * self.cell_size + 20
                
                # Draw Walls
                if maze_data.northWall[r][c]:
                    pygame.draw.line(self.screen, BLACK, (x, y), (x + self.cell_size, y), 2)
                if maze_data.eastWall[r][c]:
                    pygame.draw.line(self.screen, BLACK, (x + self.cell_size, y), (x + self.cell_size, y + self.cell_size), 2)
        
        pygame.display.flip()

    def highlight_cell(self, r, c, color=GREEN):
        """Used to show the mouse moving"""
        x = (c - 1) * self.cell_size + 20 + self.cell_size // 2
        y = (r - 1) * self.cell_size + 20 + self.cell_size // 2
        pygame.draw.circle(self.screen, color, (x, y), 8)
        pygame.display.flip()