import pygame as pg
import time


class Board:
    matrix = [[0 for _ in range(9)] for _ in range(9)]
    stop = False

    def __init__(self):
        pg.init()
        self.original_matrix = [[0 for _ in range(9)] for _ in range(9)]

        self.key_i = 0
        self.key_j = 0
        self.white = (255, 255, 255)
        self.black = (0, 0, 0)
        self.red = (255, 0, 0)
        self.gray = (67, 69, 71)
        self.green = (0, 255, 0)
        self.FPS = 13
        self.clock = pg.time.Clock()
        self.enough_no = None
        self.start = time.time()
        # Window Variables
        self.display_width = 496
        self.display_height = 496
        self.extra_space = 75
        self.display = pg.display.set_mode(
            (self.display_width, self.display_height+self.extra_space))
        # ----------------------------------
        pg.display.set_caption('Sudoku')
        while True:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    quit()
                    break
            self.display.fill(self.white)
            self.lines()
            self.print_numbers()
            self.select_block()
            self.type_stuff()
            self.highlight_box()
            self.bottom_space()
            self.highlight_key()
            if self.stop == True:
                self.check_no()
                if self.enough_no == False:
                    text_1 = "Infinite Solutions Possible"
                    text_2 = "Please Add More Valid Numbers"
                    self.print_stuff(48, text_1,
                                     self.red, 40, self.display_height // 2 - 40)
                    self.print_stuff(48, text_2,
                                     self.red, 3, self.display_height // 2 + 10)
                    end = time.time()
                    diff_time = self.start - end
                    if abs(diff_time // 2) == 2:
                        self.stop = False

            self.clock.tick(self.FPS)
            pg.display.update()

    def draw_line(self, color, x, y, width, height):
        #surface, color, (x, y, width, height)
        self.line_x = x
        self.line_y = y
        self.line_width = width
        self.line_height = height
        line = pg.draw.rect(self.display, color, (self.line_x,
                                                  self.line_y, self.line_width, self.line_height))

    def lines(self):
        self.line_distance = int(self.display_height/9)
        self.distance_covered = 0
        self.line_no = 9
        self.thick = 1

        for i in range(self.line_no):
            # Vertical
            if i == 3 or i == 6:
                self.thick = 5
            else:
                self.thick = 1
            self.draw_line(self.black, self.distance_covered, 0,
                           self.thick, self.display_height)
            # Horizontal
            self.draw_line(self.black, 0, self.distance_covered,
                           self.display_width, self.thick)
            self.distance_covered += self.line_distance

    def print_stuff(self, font_size, text, color, x, y):
        self.font = pg.font.Font(None, font_size)
        self.text_render = self.font.render(text, 1, color)
        self.display.blit(self.text_render, (x, y))

    def print_numbers(self):
        gap_horizontal = self.display_height/9
        gap_vertical = self.display_height/9

        for i in range(9):
            for j in range(9):
                n = self.matrix[i][j]
                xx = gap_horizontal*i + 0.3*gap_horizontal
                yy = gap_vertical*j + 0.3*gap_vertical
                if n != 0:
                    self.print_stuff(50, str(n), self.black, xx, yy)

    def draw_button(self, x, y, color, width, height):
        pg.draw.rect(self.display, color, (x, y, width, height))

    def bottom_space(self):
        btn_x = 330
        btn_y = self.display_height+15
        btn_width = self.display_width-335
        btn_height = 50
        self.draw_button(btn_x, btn_y,
                         self.green, btn_width, btn_height)
        self.print_stuff(40, "Solution", self.gray,
                         self.display_width-145, self.display_height+28)

        # Checking if the button is hovering over the button and if it is it will reveal the solution
        click = pg.mouse.get_pressed()
        mouse = pg.mouse.get_pos()
        mouse_x = self.mouse[0]
        mouse_y = self.mouse[1]
        # Checking If The Mouse Is Hovering Over The Button And If Clicks Then Redirect it to the Game
        if btn_x + btn_width > mouse_x > btn_x:
            if btn_y + btn_width > mouse_y > btn_y:
                if click[0] == 1:
                    self.stop = True
                    self.start = time.time()
                    self.return_sol()

        # Drawing a line for the bottom
        self.draw_line(self.black, 0, self.display_height,
                       self.display_width, 5)

        self.print_stuff(21, "Press Enter To Solve The Board",
                         self.black, 0, self.display_height+15)

        self.print_stuff(21, "The Board Should have At Least 16 Numbers",
                         self.black, 0, self.display_height+35)

        self.print_stuff(21, "Press Space To Empty The Board",
                         self.black, 0, self.display_height+55)

        self.draw_line(self.black, 320, self.display_height,
                       5, self.extra_space)

    def select_block(self):
        self.click = pg.mouse.get_pressed()
        self.mouse = pg.mouse.get_pos()

        # As we know there are three blocks each consiting of three subblocks we're gonna get the vertical and   #horizontal box one by one and then combine them to get the subblock position
        if self.click[0] == 1:
            # We're getting the which of the vertical box is being clicked through this
            ver_block = self.mouse[1] // (self.display_height // 9)
            # We're getting the which of the horizontal box is being clicked through this
            hori_block = self.mouse[0] // (self.display_width // 9)
            self.key_i = ver_block
            self.key_j = hori_block

    def type_stuff(self):
        self.keys = pg.key.get_pressed()
        # For The Upper Number Pad
        if self.key_i != None and self.key_j != None:
            if self.keys[pg.K_1]:
                self.matrix[self.key_j][self.key_i] = 1
            if self.keys[pg.K_2]:
                self.matrix[self.key_j][self.key_i] = 2
            if self.keys[pg.K_3]:
                self.matrix[self.key_j][self.key_i] = 3
            if self.keys[pg.K_4]:
                self.matrix[self.key_j][self.key_i] = 4
            if self.keys[pg.K_5]:
                self.matrix[self.key_j][self.key_i] = 5
            if self.keys[pg.K_6]:
                self.matrix[self.key_j][self.key_i] = 6
            if self.keys[pg.K_7]:
                self.matrix[self.key_j][self.key_i] = 7
            if self.keys[pg.K_8]:
                self.matrix[self.key_j][self.key_i] = 8
            if self.keys[pg.K_9]:
                self.matrix[self.key_j][self.key_i] = 9
            if self.keys[pg.K_BACKSPACE]:
                self.matrix[self.key_j][self.key_i] = 0

        # For The Right Side Number Pad
        if self.key_i != None and self.key_j != None:
            if self.keys[pg.K_KP1]:
                self.matrix[self.key_j][self.key_i] = 1
            if self.keys[pg.K_KP2]:
                self.matrix[self.key_j][self.key_i] = 2
            if self.keys[pg.K_KP3]:
                self.matrix[self.key_j][self.key_i] = 3
            if self.keys[pg.K_KP4]:
                self.matrix[self.key_j][self.key_i] = 4
            if self.keys[pg.K_KP5]:
                self.matrix[self.key_j][self.key_i] = 5
            if self.keys[pg.K_KP6]:
                self.matrix[self.key_j][self.key_i] = 6
            if self.keys[pg.K_KP7]:
                self.matrix[self.key_j][self.key_i] = 7
            if self.keys[pg.K_KP8]:
                self.matrix[self.key_j][self.key_i] = 8
            if self.keys[pg.K_KP9]:
                self.matrix[self.key_j][self.key_i] = 9
            if self.keys[pg.K_SPACE]:
                self.matrix = self.original_matrix
            if self.keys[pg.K_RETURN] or self.keys[pg.K_KP_ENTER]:
                self.start = time.time()
                self.return_sol()
                self.stop = False


    def highlight_box(self):
        cell_width = self.display_width//9
        cell_height = self.display_height//9

        #color, x, y, width, height
        if self.key_i != None and self.key_j != None and self.key_i <= 8:
            # if self.enough_no != False:
            # Top Line
            self.draw_line(self.green, self.key_j*cell_width,
                           self.key_i*cell_height, cell_width, 5)
            # Right Line
            self.draw_line(self.green, self.key_j*cell_width,
                           self.key_i*cell_height, 5, cell_width)
            # Left Line
            self.draw_line(self.green, (self.key_j*cell_width) + cell_width,
                           (self.key_i*cell_height)+cell_height, -3, -cell_width)
            # Bottom Line
            self.draw_line(self.green, (self.key_j*cell_width) + cell_width,
                           (self.key_i*cell_height)+cell_height, -cell_height, -3)

    def highlight_key(self):
        if self.keys[pg.K_UP] and self.key_i > 0:
            self.key_i -= 1
        elif self.keys[pg.K_DOWN]and self.key_i < 8:
            self.key_i += 1
        elif self.keys[pg.K_LEFT]and self.key_j > 0:
            self.key_j -= 1
        elif self.keys[pg.K_RIGHT]and self.key_j < 8:
            self.key_j += 1

    # --------------------------------------------Solver----------------------------------------------------------------------------------

    # Finding Empty Boxes(0's) in the board

    def check_time(self):
        self.solve_end = time.time()
        print(self.solve_end-self.solve_start)
        if self.solve_end-self.solve_start > 3:
            self.print_stuff(40, "Time limit exceeded", self.black, 50, 100)

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
        self.solve_end = time.time()
        diff = self.solve_end - self.solve_start
        if diff > 3:
            print("bye bye bitches");
            return False
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
        if self.stop == False:
            print("Solving the board")
            self.solve_start = time.time()
            self.solve(self.matrix)

    def check_no(self):
        count = 0
        for i in range(9):
            for j in range(9):
                if self.matrix[i][j] != 0:
                    count += 1

        if count >= 16:
            self.enough_no = True
        else:
            self.enough_no = False


# thing = Board()
