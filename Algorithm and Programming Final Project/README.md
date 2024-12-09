# Maze Profiler

The `MazeProfiler` is a Python utility designed to evaluate the performance of maze generators and solvers. It profiles the generation and solving of mazes by recording performance metrics such as execution time and solution details. It also provides functionality to save, load, and analyze profiling results.

---

## Features

- **Profile Maze Generators:** Evaluate maze generation performance.
- **Profile Maze Solvers:** Evaluate maze-solving performance and store results.
- **Data Persistence:** Save and load profiling data using pickle files.
- **Search and Filter Results:** Query generation and solver data using flexible filters.
- **Clear and Reset Data:** Manage profiling sessions effectively.
- **Statistics:** Get an overview of the profiled data.

---

## How It Works

The profiler consists of the following components:

1. **GenerationData:** Stores details about maze generation (e.g., generator name, time taken, rules used).
2. **SolverData:** Stores details about solving a maze (e.g., solver name, time taken, solution path).
3. **MazeProfiler:** The main utility that manages profiling, data persistence, and querying.

---

## Installation

Make sure you have Python 3.7+ installed. The `MazeProfiler` doesn't depend on any external library

---

## How to run
Just run the main.py