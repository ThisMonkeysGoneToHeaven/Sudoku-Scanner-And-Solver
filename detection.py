# loading necessary libraries
from PIL import Image, ImageOps, ImageEnhance, ImageDraw
import sys
import numpy
import cv2 as cv
from tensorflow.keras import models


class Detection:
    # making a board for containing potential numbers
    board = [[None for _ in range(9)] for _ in range(9)]

    def __init__(self, image_name):
        # loading the image
        self.image = Image.open(image_name).convert('RGB')  # image_name
        # resizing image upto a Good size
        self.size = (400, 400)
        self.image = self.image.resize(self.size)

        # calling the lines() function
        self.lines()

        # adding brightness to image
        enhancer = ImageEnhance.Brightness(self.image)
        self.image = enhancer.enhance(2)

        # applying adaptive thresholding using opencv
        self.cv_image = cv.cvtColor(numpy.array(self.image), cv.COLOR_RGB2GRAY)

        # mode of effects, threshing or erosion
        mode = 'thresh'

        # gausian thresh
        thresh = cv.adaptiveThreshold(
            self.cv_image, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY, 199, 5)

        # using erosion
        kernel = numpy.ones((5, 5), numpy.uint8)
        img_erosion = cv.erode(self.cv_image, kernel, iterations=1)

        # converting cv_image to PIL image back after thresholding

        if mode == 'thresh':
            self.img = cv.cvtColor(thresh, cv.COLOR_GRAY2RGB)
        else:
            self.img = cv.cvtColor(img_erosion, cv.COLOR_GRAY2RGB)
        self.image = Image.fromarray(numpy.array(self.img))

        # inverting color of the image
        if mode == "thresh":
            self.image = ImageOps.invert(self.image)
        self.image = self.image.convert('L')


        # grabbing box slices from the image for getting each number
        box_size = self.size[0]//9
        # making a grid of None's for storing box images
        self.grid = [[None for _ in range(9)] for _ in range(9)]

        # going through each box, cropping it
        # and then storing it in the grid
        for i in range(9):
            for j in range(9):
                # defining dimensions for the [i][j] box
                left = j*box_size
                right = left + box_size
                top = i*box_size
                bottom = top+box_size
                # getting its crop from the image
                this = self.image.crop((left, top, right, bottom))
                fifteen = int(box_size*0.15)
                # assigning it to the grid[i][j]
                this = this.crop(
                    (fifteen, fifteen, box_size-fifteen, box_size-fifteen))
               	self.grid[i][j] = this.resize((28, 28))

        # finding a midpoint to decide borderline whiteness, mid
        self.whites = []
        for i in range(9):
            for j in range(9):
                self.whites.append(self.whiteness(self.grid[i][j]))

        self.whites.sort()
        tempmax = -1
        rindex = None
        tsum = sum(self.whites)
        leftsum = 0
        for i in range(80):
            leftsum += self.whites[i]
            rightsum = tsum - leftsum
            avgdiff = rightsum/(81-i+1) - leftsum/(i+1)
            if avgdiff > tempmax:
                tempmax = avgdiff
                rindex = i+1
        mid = self.whites[rindex]-0.05

        # count is a variable made to count the number
        # of squares with inputs calculated by this algorithm
        count = 0
        for i in range(9):
            for j in range(9):
                self.whites = self.whiteness(self.grid[i][j])
                if self.whites > mid:
                    count += 1
                else:
                    self.board[i][j] = 0
        # print(count)

        # loading the tensorflow model stored locally
        model = models.load_model('model.h5')

        # storing all the results in board array
        for i in range(9):
            for j in range(9):
                if self.board[i][j] == None:
                	self.board[i][j] = self.recognize(model, self.grid[i][j])
        # self.print_board()

    def print_board(self):
        # printing the damn board
        for i in range(9):
            for j in range(9):
                print(self.board[i][j], end=' ')
            print('\n')

    def recognize(self, model, test):
        arr = numpy.array(test)
        arr = arr/255
        arr = arr.reshape(-1, 28, 28, 1)
        activations = model.predict(arr).tolist()[0]
        num = activations.index(max(activations))
        ## if recognized value is 0, then return second largest
        if num == 0:
        	activations[0] = -1
        	num = activations.index(max(activations))
        return num

    def whiteness(self, pic):
        self.size = pic.size
        d = 5  # defining a boundary
        pic = pic.crop((d, d, self.size[0]-d, self.size[0]-d))
        total_pixels = self.size[0]*self.size[0]
        # white_pixels = numpy.sum(numpy.array(pic)==255)
        white_pixels = numpy.sum(numpy.array(pic) > 185)
        return (white_pixels/total_pixels)

    # Removing grid lines

    def draw_line(self, x1, y1, x2, y2, w):
        shape = [(x1, y1), (x2, y2)]
        img1 = ImageDraw.Draw(self.image)
        img1.line(shape, fill="white", width=w)

    def lines(self):
        line_distance = int(self.size[1]/9)
        dis_covered = 0
        line_no = 10
        thick = 5
        for i in range(line_no):
            if i == 3 or i == 6:
                thick = 15
            else:
                thick = 15
                # Vertical
            self.draw_line(dis_covered, 0, dis_covered, self.size[1], thick)
            # Horizontal
            self.draw_line(0, dis_covered, self.size[0], dis_covered, thick)
            dis_covered += line_distance

# thing = Detection("hello")
