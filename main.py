#!/usr/bin/env python3
import sys
from maze_solver import *
from maze import Maze

run_default_algorithm = False

try:  # look if algorithm is given as argument, otherwise use default
    algorithm = sys.argv[1].upper()
    accepted_algorithms = ["DFS", "IDS", "BFS", "UCS", "ASTAR", "GREEDY"]
    if algorithm not in accepted_algorithms:  # check if algorithm is valid one
        print("Error: search algorithm (" + algorithm + ") not in the list of possible algorithms")
        print("Usage: python3 ALGORITHM [maze_file.maze]")
        accepted_algorithms.sort()
        print("Possible algorithms: " + str(accepted_algorithms))
        exit(-1)
except IndexError:
    run_default_algorithm = True
    algorithm = "BFS"

if len(sys.argv) > 2: # if maze file is given as argument, use that. Otherwise use default.maze
    maze = Maze(sys.argv[2])
else:
    maze = Maze()

maze.print_maze(True)
solve_maze_general(maze, algorithm)

if run_default_algorithm:
    print("No algorithm given as argument, used default (BFS)")
