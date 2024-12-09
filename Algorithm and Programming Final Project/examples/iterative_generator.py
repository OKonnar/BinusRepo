from core.generator import Generator
from core.generation_rules import Rules
from typing import Optional
import random

class IterativeBacktrackingGenerator(Generator):
    """Maze generator using an iterative backtracking algorithm."""

    def __init__(self):
        super().__init__()

    def generate(self, rules: Rules) -> Optional[str]:
        """Generate the maze using an iterative backtracking algorithm."""
        # Initialize the grid with walls
        grid = [[rules.wall for _ in range(rules.cols)] for _ in range(rules.rows)]

        # Stack to keep track of the current path (cells to visit)
        stack = []

        # Define the starting position (usually top-left corner)
        start_x, start_y = 0, 0
        grid[start_x][start_y] = rules.start  # Set the starting point

        # Directions for moving in the maze (down, up, right, left)
        directions = [(0, 2), (0, -2), (2, 0), (-2, 0)]
        random.shuffle(directions)  # Shuffle to randomize direction order

        # Push the start position onto the stack
        stack.append((start_x, start_y))

        # Loop until the stack is empty
        while stack:
            # Get the current cell
            current_x, current_y = stack[-1]
            # Find the neighbors that are unvisited (empty spaces)
            unvisited_neighbors = []
            for dx, dy in directions:
                nx, ny = current_x + dx, current_y + dy
                if 0 <= nx < rules.rows and 0 <= ny < rules.cols and grid[nx][ny] == rules.wall:
                    unvisited_neighbors.append((nx, ny))
            if unvisited_neighbors:
                # Pick a random neighbor to visit
                next_x, next_y = random.choice(unvisited_neighbors)
                # Mark the neighbor as part of the path
                grid[next_x][next_y] = rules.empty
                # Carve the wall between the current cell and the next cell
                grid[(current_x + next_x) // 2][(current_y + next_y) // 2] = rules.empty
                stack.append((next_x, next_y))  # Add it to the stack
            else:
                # If there are no unvisited neighbors, backtrack
                stack.pop()

        # Adjust the end position if the maze has an even number of rows or columns
        end_x, end_y = rules.rows - 1, rules.cols - 1
        grid[end_x - 1][end_y] = rules.empty
        grid[end_x][end_y - 1] = rules.empty
        grid[end_x][end_y] = rules.end

        maze_string = "\n".join("".join(row) for row in grid)
        return maze_string