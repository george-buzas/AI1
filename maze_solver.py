#!/usr/bin/env python3
from fringe import Fringe
from state import State

# implementation of IDS algorithm
def IDS(maze, fr, max_depth):
    room = maze.get_room(*maze.get_start())
    state = State(room, None)
    fr.push(state)
    room.is_visited = True
    room_array = []
    room_array.append(room)
    while not fr.is_empty():
        # get item from fringe and get the room from that state
        state = fr.pop()
        room = state.get_room()

        if room.is_goal():
            # if room is the goal, print that with the statistics and the path and return
            print("solved")
            fr.print_stats()
            state.print_path()
            state.print_actions()
            print()  # print newline
            maze.print_maze_with_path(state)
            return True

        for d in room.get_connections():
            # loop through every possible move
            new_room, cost = room.make_move(d, state.get_cost())             # Get new room after move and cost to get there
            if new_room.is_visited == False and room.depth + 1 <= max_depth: # Only pushing the new room to the fringe, if it has not been visited before
                new_state = State(new_room, state, cost)                     # Create new state with new room and old room
                new_room.depth = room.depth + 1                              # Update the depth of the current state
                fr.push(new_state)                                           # Push the new state
                new_room.is_visited = True                                   # Mark the new_room as visited, so there will not be multiple instances of the same room in the fringe
                room_array.append(new_room)                                  # If the IDS algorithm does not find a solution, we will mark all rooms added to the fringe, as not visited 
    
    for current_room in room_array:
        current_room.is_visited = False
        current_room.depth = 0

    return False


def solve_maze_general(maze, algorithm):
    """
    Finds a path in a given maze with the given algorithm
    :param maze: The maze to solve
    :param algorithm: The desired algorithm to use
    :return: True if solution is found, False otherwise
    """
    # select the right fringe for each algorithm
    if algorithm == "BFS":
        fr = Fringe("FIFO")
    elif algorithm == "DFS":
        fr = Fringe("STACK")
    elif algorithm == "UCS" or algorithm == "GREEDY" or algorithm == "ASTAR":
        fr = Fringe("PRIORITY")
    elif algorithm == "IDS":
        fr = Fringe("STACK")
        current_max_depth = 0
        while not IDS(maze, fr, current_max_depth):
            current_max_depth += 1
        return 
    else:
        print("Algorithm not found/implemented, exit")
        return

    # get the start room, create state with start room and None as parent and put it in fringe
    room = maze.get_room(*maze.get_start())
    state = State(room, None)
    fr.push(state)
    room.is_visited = True

    while not fr.is_empty():
        
        # get item from fringe and get the room from that state
        state = fr.pop()
        room = state.get_room()

        if room.is_goal():
            # if room is the goal, print that with the statistics and the path and return
            print("solved")
            fr.print_stats()
            state.print_path()
            state.print_actions()
            print()  # print newline
            maze.print_maze_with_path(state)
            return True

        for d in room.get_connections():
            # loop through every possible move
            new_room, cost = room.make_move(d, state.get_cost())        # Get new room after move and cost to get there
            if new_room.is_visited == False:                            # Only pushing the new room to the fringe, if it has not been visited before
                new_state = State(new_room, state, cost)                # Create new state with new room and old room
                fr.push(new_state)                                      # push the new state
                if algorithm == "BFS" or algorithm == "DFS":
                    new_room.is_visited = True

        if algorithm == "UCS" or algorithm == "GREEDY" or algorithm == "ASTAR":
            room.is_visited = True

    print("not solved")     # fringe is empty and goal is not found, so maze is not solved
    fr.print_stats()        # print the statistics of the fringe
    return False
