# Maze-Generator-and-Solver
## Project Overview
This project is a deep dive into computer graphics and algorithmic logic. The maze is generated usng a DFS algorithm using backtracking 
, and the solver finds a path from a start cell to an end cell using a stack-based traversal approach. 

The system also includes a graphical visualization that shows maze generation and maze solving. 

## How It Works
- The maze generated using a randomized DFS approach:
1. Start from an initial cell
2. Mark it as visited.
3. Randomly choose an unvisited neighbor.
4. Remove the wall between current and chosen cell.
5. Push current cell to a stack.
6. Move to the next cell.
7. If no visited neighbors exist, backtrack using the stack.

This process continues until all cells are visited, resulting in a perfect maze.

## Maze Representation
The maze is represented using two wall arrays:

- northWall[R][C] → controls top walls of cells
- eastWall[R][C] → controls right walls of cells

Rules:

- 1 = wall exists
- 0 = wall removed

## Maze Solving Algorithm
The solver uses a DFS backtracking strategy:

1. Start from the entry cell.
2. Move randomly to adjacent cells where no wall exists.
3. Use a stack to store the current path.
4. If a dead end is reached:
    - Mark it as visited (blue)
    - Backtrack using the stack
5. Continue until the end cell is reached

## Visualization

The visualization module displays:

- Maze grid (walls)
- Generation process (dynamic wall removal)
- Solver movement:
    - 🔴 Red dot → current path
    - 🔵 Blue cells → dead ends (backtracking)

## How to Run
1. Install dependencies
    ```pip install pygame```
2. Run the program
    ```python main.py```

## Concepts Used
- Depth-First Search (DFS)
- Stack-based backtracking
- Grid based graph representation
- Randomized traversal