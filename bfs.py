from collections import deque

def ValidMove(board, row, col, num):
    block_row, block_col = 3 * (row // 3), 3 * (col // 3)
    for k in range(9):
        if board[row][k] == num or board[k][col] == num or \
           board[block_row + k//3][block_col + k%3] == num:
            return False
    return True

def Neighbour(board):
    for x in range(9):
        for y in range(9):
            if board[x][y] == 0:
                return x, y
    return -1, -1

def solve_sudoku_bfs(board):
    queue = deque([(board, Neighbour(board))])
    while queue:
        current_board, (row, col) = queue.popleft()
        if row == -1: 
            return current_board
        for num in range(1, 10): 
            if ValidMove(current_board, row, col, num):
                new_board = [row[:] for row in current_board] 
                new_board[row][col] = num  
                next_row, next_col = Neighbour(new_board)
                queue.append((new_board, (next_row, next_col)))
    return None

board = [
    [5, 3, 0, 0, 7, 0, 0, 0, 0],
    [6, 0, 0, 1, 9, 5, 0, 0, 0],
    [0, 9, 8, 0, 0, 0, 0, 6, 0],
    [8, 0, 0, 0, 6, 0, 0, 0, 3],
    [4, 0, 0, 8, 0, 3, 0, 0, 1],
    [7, 0, 0, 0, 2, 0, 0, 0, 6],
    [0, 6, 0, 0, 0, 0, 2, 8, 0],
    [0, 0, 0, 4, 1, 9, 0, 0, 5],
    [0, 0, 0, 0, 8, 0, 0, 7, 9]
]

solved_board = solve_sudoku_bfs(board)
for line in solved_board:
    print(line)
