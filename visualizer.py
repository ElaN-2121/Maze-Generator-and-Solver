import pygame

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)


class MazeVisualizer:

    def __init__(self, screen, cell_size=25):
        self.screen = screen
        self.cell_size = cell_size

    def draw_maze(self, maze_data, start=(1, 1), end=None):
        """
        Draw maze with ONLY ONE outlet:
        TOP-LEFT opening.
        """

        self.screen.fill(WHITE)

        ROWS = maze_data.rows
        COLS = maze_data.cols
        offset = 20

        for r in range(1, ROWS + 1):
            for c in range(1, COLS + 1):

                x = (c - 1) * self.cell_size + offset
                y = (r - 1) * self.cell_size + offset

                if maze_data.north_wall[r][c]:
                    pygame.draw.line(
                        self.screen,
                        BLACK,
                        (x, y),
                        (x + self.cell_size, y),
                        2
                    )

                if maze_data.east_wall[r][c]:
                    pygame.draw.line(
                        self.screen,
                        BLACK,
                        (x + self.cell_size, y),
                        (x + self.cell_size, y + self.cell_size),
                        2
                    )

 
        start_col = start[1]

        pygame.draw.line(
            self.screen,
            BLACK,
            (offset, offset),
            (offset + (start_col - 1) * self.cell_size, offset),
            2
        )

        pygame.draw.line(
            self.screen,
            BLACK,
            (offset + start_col * self.cell_size, offset),
            (offset + COLS * self.cell_size, offset),
            2
        )

   

        bottom_y = offset + ROWS * self.cell_size

        pygame.draw.line(
            self.screen,
            BLACK,
            (offset, bottom_y),
            (offset + COLS * self.cell_size, bottom_y),
            2
        )


        pygame.draw.line(
            self.screen,
            BLACK,
            (offset, offset),
            (offset, bottom_y),
            2
        )



        pygame.draw.line(
            self.screen,
            BLACK,
            (offset + COLS * self.cell_size, offset),
            (offset + COLS * self.cell_size, bottom_y),
            2
        )

        pygame.display.flip()

    def highlight_cell(self, r, c, color=GREEN, radius=8):

        x = (c - 1) * self.cell_size + 20 + self.cell_size // 2
        y = (r - 1) * self.cell_size + 20 + self.cell_size // 2

        pygame.draw.circle(
            self.screen,
            color,
            (x, y),
            radius
        )

    def animate_generation(
        self,
        maze_data,
        current_cell,
        start=(1, 1),
        end=None
    ):

        self.draw_maze(maze_data, start, end)

        self.highlight_cell(
            current_cell[0],
            current_cell[1],
            color=GREEN,
            radius=8
        )

        pygame.display.flip()

    def animate_solver(
        self,
        maze_data,
        current_cell,
        path,
        dead_ends,
        start=(1, 1),
        end=None
    ):

        self.draw_maze(maze_data, start, end)

        for r, c in dead_ends:
            self.highlight_cell(
                r,
                c,
                color=BLUE,
                radius=5
            )

      
        for r, c in path:
            self.highlight_cell(
                r,
                c,
                color=RED,
                radius=6
            )

        self.highlight_cell(
            current_cell[0],
            current_cell[1],
            color=GREEN,
            radius=8
        )

        pygame.display.flip()
