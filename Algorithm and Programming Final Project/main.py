from core.maze_profiler import MazeProfiler
from core.generation_rules import Rules
from examples.iterative_generator import IterativeBacktrackingGenerator
from examples.dfs_solver import DFSMazeSolver
import random

def random_rules() -> Rules:
    return Rules(cols=random.randint(5, 100), rows=random.randint(5, 100))

# Here's an example on how to get started with the profiler

if __name__ == "__main__":

    profiler = MazeProfiler()

    # We can load previously saved file
    profiler.load("My super amazing file")

    # We profile the IterativeBacktrackingGenerator to generate 50 mazes with random rules
    profiler.profile_generator(IterativeBacktrackingGenerator(), lambda : random_rules(), 50)

    # Some more examples
    # profiler.profile_generator(IterativeBacktrackingGenerator(), lambda : Rules(cols=random.randint(5, 100), rows=random.randint(5, 100)), 50)
    # profiler.profile_generator(IterativeBacktrackingGenerator(), lambda : Rules(cols=26, rows=26), 50)


    # We query 10 or less result matching our lambda filter function
    queried_generation_data = profiler.search_generation_data(10, lambda generation_data : generation_data.generation_rules.rows < 30 and  generation_data.generation_rules.cols < 30)

    # Some more examples
    # queried_generation_data = profiler.search_generation_data(10)
    # queried_generation_data = profiler.search_generation_data(10, lambda generation_data : generation_data.generator_name == "IterativeBacktrackingGenerator")

    # Showcase of query
    for query_result in queried_generation_data:
        print(query_result)

    # Then we apply the solver on the queried data
    results = profiler.profile_solver(DFSMazeSolver(), queried_generation_data)

    # Showcase of result
    for result in results:
        print(result)

    # We can save files via serialization
    profiler.save("My super amazing file")