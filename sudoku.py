import math 
import random
import time

def print_board(board):
    RED = "\033[31m"
    BLACK = "\033[37m"
    
    N = len(board)
    n = math.floor(math.sqrt(N))
    assert N == n*n

    board_string = ""
    for row in range(N):
        if row > 0 and row % n == 0:
            board_string += "\n"
        for col in range(N):
            if col > 0 and col % n == 0: 
                board_string += " "
            value = board[row][col]
            if value != 0:
                board_string += RED
            else:
                board_string += BLACK
            board_string += "[{:02.0f}]".format(value)
            
        board_string += "\n" + BLACK

    print(board_string)

def make_puzzle(N):
    board = [ [0 for i in range(N)] for i in range(N)]

    allowed = [ i for i in range(1,N+1)]  # list of numbers 1 - N
    for i in range(N):
        row = random.randrange(0,N)
        col = random.randrange(0,N)
        value = random.randrange(0, len(allowed))
        board[row][col] = allowed.pop(value)
  
    row_sets = [set() for i in range(N)]
    col_sets = [set() for i in range(N)]

    for i in range(N):
        for j in range(N):
            num_col = board[j][i]
            if num_col>0:
                col_sets[i].add(num_col)
            num_row = board[i][j]
            if num_row>0:
                row_sets[i].add(num_row)

    n = math.floor(math.sqrt(N))
    reg_sets = [[set()for i in range(n)] for i in range(n)]

    for i in range(1,n+1):
        row_end = i * n 
        row_start = row_end - n
        for j in range(1,n+1):
            col_end = j * n 
            col_start = col_end - n
            for row in range(row_start,row_end):
                for col in range(col_start, col_end):
                    num = board[row][col]
                    if num > 0:
                        reg_sets[i-1][j-1].add(num)
    
    puzzle = {"board":board, "row_sets": row_sets, "col_sets": col_sets, "reg_sets": reg_sets}
    return puzzle

def get_square(puzzle, row, col):
    board = puzzle["board"]
    value = board[row][col]

    row_sets = puzzle["row_sets"]
    row_set = row_sets[row]

    col_sets = puzzle["col_sets"]
    col_set = col_sets[col]

    reg_sets = puzzle["reg_sets"]
    n = math.floor(math.sqrt(len(board)))

    for i in range(1,n+1):
        row_end = i * n 
        row_start = row_end - n
        for j in range(1,n+1):
            col_end = j * n 
            col_start = col_end - n
            if (row in range(row_start, row_end)) and (col in range(col_start, col_end)):
                reg_set = reg_sets[i-1][j-1]
    
    square = {"value": value, "row_set": row_set, "col_set": col_set, "reg_set": reg_set}
    return square

def move(puzzle, row, col, new_value):
    square = get_square(puzzle, row, col)
    board = puzzle["board"]
    row_set = square["row_set"]
    col_set = square["col_set"]
    n = math.floor(math.sqrt(len(board)))

    in_rows = False
    in_cols = False
    in_regs = False


    if square["value"] == 0:
        for value in row_set:
            if new_value == value:
                in_rows = True
        for value in col_set:
            if new_value == value:
                in_cols = True
        for i in range(1,n+1):
            row_end = i * n 
            row_start = row_end - n
            if row >= row_start and row < row_end:
                for j in range(1,n+1):
                    col_end = j * n 
                    col_start = col_end - n
                    if col >= col_start and col < col_end:
                        for x in range(row_start,row_end):
                            for y in range(col_start, col_end):
                                num = board[x][y]
                                if new_value == num:
                                    in_regs = True
        if in_rows == False and in_cols == False and in_regs==False:
            board[row][col] = new_value
            return True
        else:
            return False
    else: 
        return False

def fill_puzzle(puzzle):
    board = puzzle["board"]
    N = len(board)

    count = 0                   # to find how much of board is already filled
    for row in board:
        for value in row:
            if value != 0:
                count +=1
    attempts = 0
    while True:
        # percentage = count/(N*N)
        if attempts <= N**4:
            if count < 0.93*(N*N):
                digit = random.randint(1, N)
                row = random.randrange(0, N)
                col = random.randrange(0, N)
                if move(puzzle, row, col, digit) != False:
                    count+=1
                attempts +=1
            else:
                break
    return count/(N*N)

def main():
    N = 9
    print("Board size:", N, "x", N)
    puzzle = make_puzzle(N)
    print("Initial puzzle:")
    for value in puzzle:
        if value == "board":
            for row in puzzle[value]:
                print(row)
            print()
        else:
            print(value, ":")
            print(puzzle[value])
            print()
    # print(puzzle)
    print("Initial board:")
    print_board(puzzle['board'])

    start = time.perf_counter()
    percentage = fill_puzzle(puzzle)
    stop = time.perf_counter()
    elapsed = stop - start

    print("\n\nFinal puzzle:")
    for value in puzzle:
        if value == "board":
            for row in puzzle[value]:
                print(row)
            print()
        else:
            print(value, ":")
            print(puzzle[value])
            print()
    print("Final board:")
    print_board(puzzle['board'])
    print("\n", percentage*100, "% of the board is filled", sep = "")
    print("Elapsed time to fill board =", elapsed,"seconds.")

main()

"""
expected time complexities:
move() - O(1)
fill() - O(n^2)
"""