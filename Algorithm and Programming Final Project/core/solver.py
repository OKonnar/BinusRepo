from core.generation_rules import Rules
from abc import ABC, abstractmethod
from typing import List, Tuple, Optional

class Solver(ABC):
    """Abstract base class for maze solving algorithms."""
    def __init__(self):
        pass

    @abstractmethod
    def solve(self, maze : str, rules : Rules) -> Optional[List[Tuple[int, int]]]:
        """Abstract method to solve the maze. Must be implemented by subclasses."""
        pass


