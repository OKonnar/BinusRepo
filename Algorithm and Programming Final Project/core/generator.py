from core.generation_rules import Rules
from abc import ABC, abstractmethod
from typing import Optional

class Generator(ABC):
    """Abstract base class for maze generation algorithms."""
    def __init__(self):
        pass

    @abstractmethod
    def generate(self, rules : Rules) -> Optional[str]:
        """Abstract method to generate the maze. Must be implemented by subclasses."""
        pass