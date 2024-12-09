from core.generator import Generator
from core.solver import Solver
from core.generation_rules import Rules
from typing import List, Tuple, Callable
import os
import time
import pickle

class SolverData:
    def __init__(self, name : str, time : float, solution : List[Tuple[int, int]]):
        """
        Initialize a SolverData object.

        Args:
            name (str): The name of the solver.
            time (float): The time taken by the solver to solve the maze.
            solution (List[Tuple[int, int]]): The solution path as a list of coordinates.
        """
        self.solver_name : str = name
        self.solver_time : float = time
        self.solution : List[Tuple[int, int]] = solution

    def to_dict(self):
        """
        Convert the SolverData object into a dictionary.

        Returns:
            dict: A dictionary representation of the SolverData object.
        """
        return {
            'solver_name': self.solver_name,
            'solver_time': self.solver_time,
            'solution': self.solution
        }

    @classmethod
    def from_dict(cls, data: dict):
        """
        Create a SolverData object from a dictionary.

        Args:
            data (dict): The dictionary containing solver data.

        Returns:
            SolverData: A SolverData object initialized with the dictionary data.
        """
        obj = cls()
        obj.solver_name = data.get('solver_name')
        obj.solver_time = data.get('solver_time', 0)
        obj.solution = data.get('solution', [])
        return obj

    def __str__(self):
        """
        Return a string representation of the SolverData object.

        Returns:
            str: A summary of the Solver data.
        """
        return (f"Solver Name: {self.solver_name}\n"
                f"Solving Time: {self.solver_time:.2f} seconds\n"
                f"Solution: {self.solution}\n")

class GenerationData:
    def __init__(self, name : str, time : float, rules : Rules, maze : str):
        """
        Initialize a GenerationData object.

        Args:
            name (str): The name of the generator.
            time (float): The time taken to generate the maze.
            rules (Rules): The rules used for generating the maze.
            maze (str): The generated maze.
        """
        self.generator_name : str = name
        self.generation_time : float = time
        self.generation_rules : Rules = rules
        self.maze : str = maze
        self.solutions : List[SolverData] = []

    def to_dict(self):
        """
        Create a GenerationData object from a dictionary.

        Args:
            data (dict): The dictionary containing generation data.

        Returns:
            GenerationData: A GenerationData object initialized with the dictionary data.
        """
        return {
            'generator_name': self.generator_name,
            'generation_time': self.generation_time,
            'generation_rules': self.generation_rules,
            'maze': self.maze,
            'solutions': [solution.to_dict() for solution in self.solutions]
        }

    @classmethod
    def from_dict(cls, data: dict):
        obj = cls()
        obj.generator_name = data.get('generator_name')
        obj.generation_time = data.get('generation_time', 0)
        obj.generation_rules = data.get('generation_rules')
        obj.maze = data.get('maze', '')
        obj.solutions = [SolverData.from_dict(s) for s in data.get('solutions', [])]
        return obj

    def add_solution(self, solution : SolverData):
        """
        Add a solver's solution to the GenerationData.

        Args:
            solution (SolverData): The solution to add.
        """
        self.solutions.append(solution)

    def __str__(self):
        """
        Return a string representation of the GenerationData object.

        Returns:
            str: A summary of the generation data.
        """
        solutions_count = len(self.solutions)
        return (f"Generator Name: {self.generator_name}\n"
                f"Generation Time: {self.generation_time:.2f} seconds\n"
                f"Generation Rules: {self.generation_rules}\n"
                f"{self.maze}\n"
                f"Number of Solutions: {solutions_count}")


class MazeProfiler:
    def __init__(self):
        """
        Initialize the MazeProfiler
        """
        self.mazes: List[GenerationData] = []

    def profile_generator(self, generator : Generator, rule_function: Callable[[], Rules] = lambda : Rules(), x_time : int = 1):
        """
        Profile a maze generator by generating mazes and recording data.

        Args:
            generator (Generator): The maze generator to profile.
            rules (Rules): The rules to use for maze generation.
            x_time (int, optional): The number of times to generate the maze. Defaults to 1.

        Returns:
            List[GenerationData]: A list of GenerationData objects for each run.
        """
        if not isinstance(generator, Generator):
            raise TypeError("The generator must be an instance of a subclass of `Generator`.")

        result : List[GenerationData] = []
        for i in range(x_time):
            rules = rule_function()
            start_time = time.time()
            maze = generator.generate(rules)
            end_time = time.time()
            time_taken = end_time - start_time
            result.append(GenerationData(generator.__class__.__name__, time_taken, rules, maze))
            self.mazes.append(GenerationData(generator.__class__.__name__, time_taken, rules, maze))
        return result

    def profile_solver(self, solver : Solver, gen_results : List[GenerationData], x_time : int = 1):
        """
        Profile a maze solver by solving generated mazes and recording data.

        Args:
            solver (Solver): The maze solver to profile.
            gen_results (List[GenerationData]): The generated mazes to solve.
            x_time (int, optional): The number of times to solve each maze. Defaults to 1.

        Returns:
            List[SolverData]: A list of SolverData objects for each run.
        """
        if not isinstance(solver, Solver):
            raise TypeError("The solver must be an instance of a subclass of `Solver`.")

        result : List[SolverData] = []
        for gen_result in gen_results:
            for x in range(x_time):
                start_time = time.time()
                solution = solver.solve(gen_result.maze, gen_result.generation_rules)
                end_time = time.time()
                time_taken = end_time - start_time
                gen_result.add_solution(SolverData(solver.__class__.__name__, time_taken, solution))
                result.append(SolverData(solver.__class__.__name__, time_taken, solution))
        return result

    def save(self, file_path: str):
        """
        Save the maze data to the specified file.

        Args:
            file_path (str): The file path to save the data.
        """
        try:
            full_path = os.path.abspath(file_path)
            with open(full_path, "wb") as f:
                pickle.dump(self.mazes, f)
            print(f"Data successfully saved to {full_path}.")
        except Exception as e:
            print(f"Error saving data to {file_path}: {e}")
            import traceback
            traceback.print_exc()  # This will print the full stack trace

    def load(self, file_path: str):
        """
        Load maze data from the specified file.

        Args:
            file_path (str): The file path to load the data from.
        """
        try:
            with open(file_path, "rb") as f:
                self.mazes = pickle.load(f)
            print(f"Data successfully loaded from {file_path}.")
        except FileNotFoundError:
            print(f"No existing data found at {file_path}.")
        except Exception as e:
            print(f"Error loading data from {file_path}: {e}")

    def search_generation_data(self, n : int = 0, filter_function: Callable[[GenerationData], bool] = lambda maze : True):
        """
        Retrieve generation data with optional filtering and limiting.

        Args:
            n (int, optional): Maximum number of results to return. Defaults to 0 (no limit).
            filter_function (Callable, optional): A function to filter generation data. Defaults to all data.

        Returns:
            List[GenerationData]: A list of filtered generation data.
        """
        result: List[GenerationData] = []
        count = 0
        for maze in self.mazes:
            if filter_function is None or filter_function(maze):
                result.append(maze)
                count += 1
            if n > 0 and count >= n:
                break

        return result

    def search_solver_data(self, n: int = 0, filter_function: Callable[[SolverData], bool] = lambda solver: True):
        """
        Retrieve solver results with optional filtering and limiting.

        Args:
            n (int, optional): Maximum number of results to return. Defaults to 0 (no limit).
            filter_function (Callable, optional): A function to filter solver results.
                                                Defaults to a function that returns True for all results.

        Returns:
            List[SolverData]: A list of filtered solver results.
        """
        result: List[SolverData] = []
        count = 0

        for maze in self.mazes:
            for solver_result in maze.solutions:
                if filter_function is None or filter_function(solver_result):
                    result.append(solver_result)
                    count += 1

                if n > 0 and count >= n:
                    return result

        return result

    def stats(self):
        return (f"{len(self.mazes)} mazes loaded.")

    def clear(self):
        print(f"Cleared {len(self.mazes)} mazes.")
        self.mazes.clear()
