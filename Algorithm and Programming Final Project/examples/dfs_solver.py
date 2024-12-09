from core.generation_rules import Rules
from core.solver import Solver
from typing import List, Tuple, Optional

class DFSMazeSolver(Solver):
    """Maze solver using depth-first search (DFS)."""

    def __init__(self):
        super().__init__()

    def solve(self, maze: str, rules: Rules) -> Optional[List[Tuple[int, int]]]:
        """
        Solve the maze using depth-first search (DFS) algorithm.

        Args:
            maze (str): The maze represented as a string.
            rules (Rules): The generation rules to understand maze structure.

        Returns:
            Optional[List[Tuple[int, int]]]: The solution path as a list of (x, y) tuples or None if no solution.
        """
        # Convert maze string into a 2D grid of characters
        grid = [list(line) for line in maze.split("\n")]

        start = None
        for x in range(rules.rows):
            for y in range(rules.cols):
                if grid[x][y] == rules.start:
                    start = (x, y)
                    break
            if start:
                break

        if not start:
            return None  # No start point found in the maze

        # Stack for DFS (starting with the start point)
        stack = [start]
        # To track visited cells
        visited = set()
        visited.add(start)

        # Directions for movement (down, up, right, left)
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]

        # Path tracking
        parent_map = {}

        while stack:
            current_x, current_y = stack[-1]

            # If we reach the end point (usually marked as 'E')
            if grid[current_x][current_y] == rules.end:
                # Reconstruct the path from end to start using parent_map
                path = []
                while (current_x, current_y) != start:
                    path.append((current_x, current_y))
                    current_x, current_y = parent_map[(current_x, current_y)]
                path.append(start)
                path.reverse()  # Reverse to get the path from start to end
                return path

            # Explore neighbors
            for dx, dy in directions:
                nx, ny = current_x + dx, current_y + dy

                # Ensure we stay within bounds and haven't visited this cell
                if 0 <= nx < rules.rows and 0 <= ny < rules.cols:
                    if grid[nx][ny] in [rules.empty, rules.end] and (nx, ny) not in visited:
                        # Mark the cell as visited and add to the stack
                        visited.add((nx, ny))
                        stack.append((nx, ny))
                        parent_map[(nx, ny)] = (current_x, current_y)
                        break  # Only move to one neighbor at a time, like DFS
            else:
                # Backtrack if no valid neighbors
                stack.pop()

        return None  # No solution found
