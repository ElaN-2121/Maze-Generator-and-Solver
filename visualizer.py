#visualizer.py
import pygame

# Standard Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

class MazeVisualizer:
    def __init__(self, screen, cell_size=25):
        """
        Initializes the visualizer.
        :param screen: The pygame display surface.
        :param cell_size: Size of each maze cell in pixels.
        """
        self.screen = screen
        self.cell_size = cell_size

    def draw_maze(self, maze_data):
        """
        Draws the maze walls and outer boundary.
        maze_data must contain: northWall, eastWall, ROWS, COLS
        """
        self.screen.fill(WHITE)
        ROWS = maze_data.ROWS
        COLS = maze_data.COLS

        # Draw inner walls
        for r in range(1, ROWS + 1):
            for c in range(1, COLS + 1):
                x = (c - 1) * self.cell_size + 20
                y = (r - 1) * self.cell_size + 20
                
                if maze_data.northWall[r][c]:
                    pygame.draw.line(self.screen, BLACK, (x, y), (x + self.cell_size, y), 2)
                if maze_data.eastWall[r][c]:
                    pygame.draw.line(self.screen, BLACK, (x + self.cell_size, y), (x + self.cell_size, y + self.cell_size), 2)
        
        # Draw outer boundary
        pygame.draw.rect(self.screen, BLACK, (20, 20, COLS * self.cell_size, ROWS * self.cell_size), 2)
        pygame.display.flip()

    def highlight_cell(self, r, c, color=GREEN, radius=8):
        """Helper to draw a circle in a cell"""
        x = (c - 1) * self.cell_size + 20 + self.cell_size // 2
        y = (r - 1) * self.cell_size + 20 + self.cell_size // 2
        pygame.draw.circle(self.screen, color, (x, y), radius)

    def animate_generation(self, maze_data, current_cell):
        """Called by Person 4 to visualize maze growth"""
        self.draw_maze(maze_data)
        self.highlight_cell(current_cell[0], current_cell[1], color=GREEN)
        pygame.display.flip()

    def animate_solver(self, maze_data, current_cell, path, dead_ends):
        """Called by Person 5 to visualize pathfinding"""
        self.draw_maze(maze_data)
        
        # Draw dead ends (blue)
        for r, c in dead_ends:
            self.highlight_cell(r, c, color=BLUE, radius=5)
            
        # Draw path (red)
        for r, c in path:
            self.highlight_cell(r, c, color=RED, radius=6)
            
        # Draw current mouse position (green)
        self.highlight_cell(current_cell[0], current_cell[1], color=GREEN, radius=8)
        pygame.display.flip()
