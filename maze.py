# maze.py

class Maze:
    def __init__(self, rows=12, cols=16):
        self.rows = rows
        self.cols = cols
        self.r = rows + 1
        self.c = cols + 1
        self.north_wall = [[1] * self.c for _ in range(self.r)]
        self.east_wall = [[1] * self.c for _ in range(self.r)]
        self.visited = [[False] * self.c for _ in range(self.r)]
        self.start = None
        self.end = None

    def initialize_all_walls(self):
        for r in range(1, self.rows + 1):
            for c in range(1, self.cols + 1):
                self.north_wall[r][c] = 1
                self.east_wall[r][c] = 1
                self.visited[r][c] = False

    def is_wall(self, r, c, direction):
        if direction == 'N':
            return r == 1 or self.north_wall[r][c] == 1
        elif direction == 'S':
            return r == self.rows or self.north_wall[r + 1][c] == 1
        elif direction == 'W':
            return c == 1 or self.east_wall[r][c - 1] == 1
        elif direction == 'E':
            return c == self.cols or self.east_wall[r][c] == 1
        else:
            raise ValueError("Direction must be N, S, E, W")

    def remove_wall_between(self, r1, c1, r2, c2):
        if r1 == r2 and abs(c1 - c2) == 1:
            if c2 == c1 + 1:
                self.east_wall[r1][c1] = 0
            else:
                self.east_wall[r1][c2] = 0
        elif c1 == c2 and abs(r1 - r2) == 1:
            if r2 == r1 + 1:
                self.north_wall[r2][c2] = 0
            else:
                self.north_wall[r1][c1] = 0
        else:
            raise ValueError("Cells are not neighbors")

    def get_adjacent_cells(self, r, c):
        neighbors = []
        if r > 1:
            neighbors.append((r - 1, c, 'N'))
        if r < self.rows:
            neighbors.append((r + 1, c, 'S'))
        if c > 1:
            neighbors.append((r, c - 1, 'W'))
        if c < self.cols:
            neighbors.append((r, c + 1, 'E'))
        return neighbors

    def get_open_neighbors(self, r, c):
        open_nbrs = []
        for nr, nc, d in self.get_adjacent_cells(r, c):
            if not self.is_wall(r, c, d):
                open_nbrs.append((nr, nc, d))
        return open_nbrs

    def is_perfect(self):
        from collections import deque
        visited = [[False] * (self.cols + 1) for _ in range(self.rows + 1)]
        q = deque()
        q.append((1, 1))
        visited[1][1] = True
        count = 0
        while q:
            r, c = q.popleft()
            count += 1
            for nr, nc, _ in self.get_open_neighbors(r, c):
                if not visited[nr][nc]:
                    visited[nr][nc] = True
                    q.append((nr, nc))
        return count == self.rows * self.cols