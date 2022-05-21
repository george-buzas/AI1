from ast import operator
from distutils.fancy_getopt import OptionDummy
import sys
import random
import operator
import math


MAXQ = 100


def in_conflict(column, row, other_column, other_row):
    """
    Checks if two locations are in conflict with each other.
    :param column: Column of queen 1.
    :param row: Row of queen 1.
    :param other_column: Column of queen 2.
    :param other_row: Row of queen 2.
    :return: True if the queens are in conflict, else False.
    """
    if column == other_column:
        return True  # Same column
    if row == other_row:
        return True  # Same row
    if abs(column - other_column) == abs(row - other_row):
        return True  # Diagonal

    return False


def in_conflict_with_another_queen(row, column, board):
    """
    Checks if the given row and column correspond to a queen that is in conflict with another queen.
    :param row: Row of the queen to be checked.
    :param column: Column of the queen to be checked.
    :param board: Board with all the queens.
    :return: True if the queen is in conflict, else False.
    """
    for other_column, other_row in enumerate(board):
        if in_conflict(column, row, other_column, other_row):
            if row != other_row or column != other_column:
                return True
    return False


def count_conflicts(board):
    """
    Counts the number of queens in conflict with each other.
    :param board: The board with all the queens on it.
    :return: The number of conflicts.
    """
    cnt = 0

    for queen in range(0, len(board)):
        for other_queen in range(queen+1, len(board)):
            if in_conflict(queen, board[queen], other_queen, board[other_queen]):
                cnt += 1

    return cnt


def evaluate_state(board):
    """
    Evaluation function. The maximal number of queens in conflict can be 1 + 2 + 3 + 4 + .. +
    (nquees-1) = (nqueens-1)*nqueens/2. Since we want to do ascending local searches, the evaluation function returns
    (nqueens-1)*nqueens/2 - countConflicts().

    :param board: list/array representation of columns and the row of the queen on that column
    :return: evaluation score
    """
    return (len(board)-1)*len(board)/2 - count_conflicts(board)


def print_board(board):
    """
    Prints the board in a human readable format in the terminal.
    :param board: The board with all the queens.
    """
    print("\n")

    for row in range(len(board)):
        line = ''
        for column in range(len(board)):
            if board[column] == row:
                line += 'Q' if in_conflict_with_another_queen(row, column, board) else 'q'
            else:
                line += '.'
        print(line)


def init_board(nqueens):
    """
    :param nqueens integer for the number of queens on the board
    :returns list/array representation of columns and the row of the queen on that column
    """

    board = []

    for column in range(nqueens):
        board.append(random.randint(0, nqueens-1))

    return board


"""
------------------ Do not change the code above! ------------------
"""


def random_search(board):
    """
    This function is an example and not an efficient solution to the nqueens problem. What it essentially does is flip
    over the board and put all the queens on a random position.
    :param board: list/array representation of columns and the row of the queen on that column
    """

    i = 0
    optimum = (len(board) - 1) * len(board) / 2

    while evaluate_state(board) != optimum:
        i += 1
        print('iteration ' + str(i) + ': evaluation = ' + str(evaluate_state(board)))
        if i == 1000:  # Give up after 1000 tries.
            break

        for column, row in enumerate(board):  # For each column, place the queen in a random row
            board[column] = random.randint(0, len(board)-1)

    if evaluate_state(board) == optimum:
        print('Solved puzzle!')

    print('Final state is:')
    print_board(board)


def hill_climbing(board):
    """
    Implement this yourself.
    :param board:
    :return:
    """
    i = 0
    optimum = (len(board) - 1) * len(board) / 2

    while evaluate_state(board) != optimum:
        i += 1
        print('iteration ' + str(i) + ': evaluation = ' + str(evaluate_state(board)))
        if i == 1000:  # Give up after 1000 tries.
            break
        best = 0
        for queen in range(0, len(board)):
            original_position = board[queen]
            for row in range(0, len(board)):
                board[queen] = row
                state = evaluate_state(board)
                if state > best:
                    best = state
                    best_col = queen
                    best_row = row
                if state == best and random.randint(0, 1) == 1:
                    best = state
                    best_col = queen
                    best_row = row

            board[queen] = original_position
        if best <= evaluate_state(board):
            break

        board[best_col] = best_row

    if evaluate_state(board) == optimum:
        print('Solved puzzle!')
    
    print('Final state is:')
    print_board(board) 


# this function creates a child from the provided 2 parents.
def reproduce(parent_1, parent_2, n_queens):
    n = n_queens
    c = random.randint(0, n - 1)
    child = parent_1[0 : c] + parent_2[c : n]
    return child

# Mutation
def mutation(child, n_queens):
    fixed_probability = 0.2
    random_probability = random.uniform(0, 1)

    if fixed_probability < random_probability : # mutation
        queen = random.randint(0, n_queens - 1)
        row = random.randint(0, n_queens - 1)
        child[queen] = row
        print_board(child)
    return child

# Verify if a child is a solution
def check_solution(child, optimum):
    if evaluate_state(child) == optimum:
        print('Solved puzzle!')
        print('Final state is:')
        print_board(child)   
        return True
    return False

def genetic_algorithm(board, n_queens):
    # initial population
    population = list()
    size = 50
    for index in range(0, size):
        population.append(init_board(n_queens))
    
    i = 0
    optimum = (len(board) - 1) * len(board) / 2
    while evaluate_state(board) != optimum:
        i += 1
        print('iteration ' + str(i))
        if i == 1000:  # Give up after 1000 tries.
            break
        new_population = list()

        # Calculate the fitness level of each individual in the population
        # We always want to select as parents, only half of the population that has the biggest fitness level
        fitness_level = list()
        for individual in range(0, size):
            fitness_level.append(evaluate_state(population[individual]))
        
        indices = list()
        for index in range (0, size):
            indices.append(index)

        population_fitness = list(zip(fitness_level, indices))

        # Sort the population based on the heursitic value(i.e. fitness level)
        sorted_population = sorted(population_fitness, key = operator.itemgetter(0))
        #print("final list - ", str(sorted_population))

        # Pick only half of the population - best #half elements from the initial population
        half_size = math.floor(size / 2)
        half_population = list()
        for individual in range (half_size, size):
            #print(sorted_population[individual][0], sorted_population[individual][1])
            half_population.append(population[sorted_population[individual][1]])
        
        # Regarding the crossover, we pick a pair of parents.
        # Each pair of parents creates always two children.
        # The reason for this is the following:
        # Since we always pick only the best half of the current population, if we were to create
        # only 1 child then, at each iteration the size of the population would decrease by half.
        # But if we choose to create always two children, then the size of the population will be the same
        # as the size of the initial population, regardless of how many iterations were done up until that point. 
        # If only 1 child is created, and if we always pick the best half of the population,
        # then after log(population_size) iterations there would be no population(i.e. the population size would be 0).
        for j in range(0, half_size):
            parent_1 = random.choice(half_population)
            parent_2 = random.choice(half_population)
            child_1 = reproduce(parent_1, parent_2, n_queens)
            child_2 = reproduce(parent_2, parent_1, n_queens)

            child_1 = mutation(child_1, n_queens)
            print('Child 1 evaluation = ' + str(evaluate_state(child_1)))
            if check_solution(child_1, optimum) == True:
                return

            child_2 = mutation(child_2, n_queens)
            print('Child 2 evaluation = ' + str(evaluate_state(child_2)))
            if check_solution(child_2, optimum) == True:
                return

            # if the current children are not a solution, add them to the new population
            new_population.append(child_1)    
            new_population.append(child_2)

        population = new_population

def simulated_annealing(board):
    """
    Implement this yourself.
    :param board:
    :return:
    """
    pass


def main():
    """
    Main function that will parse input and call the appropriate algorithm. You do not need to understand everything
    here!
    """

    try:
        if len(sys.argv) != 2:
            raise ValueError

        n_queens = int(sys.argv[1])
        if n_queens < 1 or n_queens > MAXQ:
            raise ValueError

    except ValueError:
        print('Usage: python n_queens.py NUMBER')
        return False

    print('Which algorithm to use?')
    algorithm = input('1: random, 2: hill-climbing, 3: simulated annealing, 4: genetic algorithm \n')

    try:
        algorithm = int(algorithm)

        if algorithm not in range(1, 5):
            raise ValueError

    except ValueError:
        print('Please input a number in the given range!')
        return False

    board = init_board(n_queens)
    print('Initial board: \n')
    print_board(board)

    if algorithm == 1:
        random_search(board)
    if algorithm == 2:
        hill_climbing(board)
    if algorithm == 3:
        simulated_annealing(board)
    if algorithm == 4:
        genetic_algorithm(board, n_queens)


# This line is the starting point of the program.
if __name__ == "__main__":
    main()
