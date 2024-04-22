import numpy as np
import random
import math

def InitialSolution(board):
    size = 9
    subgrid_size = 3
    filled = np.copy(board)

    for sub_x in range(0, size, subgrid_size):
        for sub_y in range(0, size, subgrid_size):
            subgrid = filled[sub_x:sub_x+subgrid_size, sub_y:sub_y+subgrid_size]
            missing = set(range(1, 10)) - set(subgrid.flatten())
            missing = list(missing)
            random.shuffle(missing)

            for i in range(subgrid_size):
                for j in range(subgrid_size):
                    if filled[sub_x+i][sub_y+j] == 0:
                        filled[sub_x+i][sub_y+j] = missing.pop()
    return filled

def Cost(board):
    cost = 0
    size = 9
    for i in range(size):
        row_cost = 9 - len(set(board[i, :]))
        col_cost = 9 - len(set(board[:, i]))
        cost += row_cost + col_cost
    return cost

def Neighbour(board):
    size = 9
    subgrid_size = 3
    x = random.randint(0, subgrid_size - 1) * subgrid_size
    y = random.randint(0, subgrid_size - 1) * subgrid_size

    i1, j1 = random.randint(0, subgrid_size - 1), random.randint(0, subgrid_size - 1)
    i2, j2 = random.randint(0, subgrid_size - 1), random.randint(0, subgrid_size - 1)
    while i1 == i2 and j1 == j2:
        i2, j2 = random.randint(0, subgrid_size - 1), random.randint(0, subgrid_size - 1)

    new_board = np.copy(board)
    # Swap two cells
    new_board[x+i1, y+j1], new_board[x+i2, y+j2] = new_board[x+i2, y+j2], new_board[x+i1, y+j1]
    return new_board

def SimAnnealing(board):
    current = InitialSolution(board)
    current_cost = Cost(current)
    temperature = 1.0
    cooling_rate = 0.99
    min_temperature = 0.01

    while temperature > min_temperature:
        next_board = Neighbour(current)
        next_cost = Cost(next_board)
        cost_diff = next_cost - current_cost

        if cost_diff < 0 or random.random() < math.exp(-cost_diff / temperature):
            current = next_board
            current_cost = next_cost

        temperature *= cooling_rate

    return current

# Example usage
board = np.array([
    [5, 3, 0, 0, 7, 0, 0, 0, 0],
    [6, 0, 0, 1, 9, 5, 0, 0, 0],
    [0, 9, 8, 0, 0, 0, 0, 6, 0],
    [8, 0, 0, 0, 6, 0, 0, 0, 3],
    [4, 0, 0, 8, 0, 3, 0, 0, 1],
    [7, 0, 0, 0, 2, 0, 0, 0, 6],
    [0, 6, 0, 0, 0, 0, 2, 8, 0],
    [0, 0, 0, 4, 1, 9, 0, 0, 5],
    [0, 0, 0, 0, 8, 0, 0, 7, 9]
])
solution = SimAnnealing(board)
print("Solved Board:")
print(solution)
