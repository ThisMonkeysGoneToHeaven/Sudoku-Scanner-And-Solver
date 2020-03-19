import time
board = [
    [1, 0, 0, 0, 4, 0, 0, 0, 0],
    [0, 9, 2, 6, 0, 0, 3, 0, 0],
    [3, 0, 0, 0, 0, 5, 1, 0, 0],
    [0, 7, 0, 1, 0, 0, 0, 0, 4],
    [0, 0, 4, 0, 5, 0, 6, 0, 0],
    [2, 0, 0, 0, 0, 4, 0, 8, 0],
    [0, 0, 9, 4, 0, 0, 0, 0, 1],
    [0, 0, 8, 0, 0, 6, 5, 2, 0],
    [0, 0, 0, 0, 1, 0, 0, 0, 6]
]


class Solve_it:
    # Just printing the board

    def print_board(self, board):
        for i in range(len(board)):
            if i % 3 == 0 and i != 0:
                print('-'*len(board[i])*3)
            for j in range((len(board[i]))):
                if j == len(board[i])-1:
                    print(board[i][j], end="\n")
                else:
                    if j == 2 or j == 5:
                        print(board[i][j], end="|")
                    else:
                        print(board[i][j], end="  ")

    # Finding Empty Boxes(0's) in the board

    def find_empty(self, board):
        for i in range(len(board)):
            for j in range(len(board)):
                if board[i][j] == 0:
                    return i, j
        return None

    # Checking if the number entered is the correct number

    def valid(self, board, pos_y, pos_x, num):
        # Checking Each Row
        for i in range(len(board[0])):
            if board[pos_y][i] == num and pos_x != i:
                return False

        # Check column
        for i in range(len(board)):
            if board[i][pos_x] == num and pos_y != i:
                return False

        # Checking id Each Square box or grid has the same number
        box_y = pos_y // 3
        box_x = pos_x // 3

        for i in range(box_y * 3, box_y*3+3):
            for j in range(box_x * 3, box_x*3+3):
                if board[i][j] == num and (i, j) != (pos_x, pos_y):
                    return False

        return True

    def solve(self, board):
        # Finding the empty place in the board
        find = self.find_empty(board)
        # If not a single empty place is found that means that the solution is completed so return True which means that it'll end the program
        if not find:
            return True
        # If there is a empty place then apply backtrackting
        row, col = find
        # we're trying to take each number from 1 to 10 and then checking if the number is good at that place or not
        for i in range(1, 10):
            # if valid just put it their
            if self.valid(board, row, col, i):
                board[row][col] = i
                # just recalling the function again and ending this one(through return True)
                if self.solve(board):
                    return True
            # if solve isn't true then this will happen
            board[row][col] = 0
        return False

    def return_sol(self):
        global time
        self.print_board(board)
        print('\n')
        print('_'*35+'\n')
        start = time.time()
        self.solve(board)
        end = time.time()
        self.print_board(board)
        time = round(end-start, 2)
        print(f"Time Taken: {time} Seconds")


solving = Solve_it()
solving.return_sol()
