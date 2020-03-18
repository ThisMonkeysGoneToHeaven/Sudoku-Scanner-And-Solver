# loading necessary libraries
import sys
import numpy
import cv2 as cv
from tensorflow.keras import models
from PIL import Image, ImageOps, ImageEnhance, ImageDraw

def recognize(model, test):
	arr = numpy.array(test)
	arr = arr/255
	arr = arr.reshape(-1,28,28,1)
	num = numpy.argmax(model.predict(arr))
	return num

def whiteness(pic):
	size = pic.size[0]
	d= 5 ## defining a boundary
	pic = pic.crop((d, d, size-d, size-d))
	total_pixels = size*size
	# white_pixels = numpy.sum(numpy.array(pic)==255)
	white_pixels = numpy.sum(numpy.array(pic) > 185)
	return (white_pixels/total_pixels)

## Removing grid lines
def draw_line(x1, y1, x2, y2, w):
    shape = [(x1, y1), (x2, y2)]
    img1 = ImageDraw.Draw(image)
    img1.line(shape, fill="white", width=w)

def lines():
    line_distance = int(size[1]/9)
    dis_covered = 0
    line_no = 10
    thick = 5
    for i in range(line_no):
        if i == 3 or i == 6:
            thick = 15
        else:
            thick = 15
            # Vertical
        draw_line(dis_covered, 0, dis_covered, size[1], thick)
        # Horizontal
        draw_line(0, dis_covered, size[0], dis_covered, thick)
        dis_covered += line_distance


## loading the image
image = Image.open('image.jpg').convert('RGB')

# resizing image upto a Good size
size = (400,400)
image = image.resize(size)

# calling the lines() function
lines()

# adding brightness to image
enhancer = ImageEnhance.Brightness(image)
image = enhancer.enhance(2)

## applying adaptive thresholding using opencv
cv_image = cv.cvtColor(numpy.array(image), cv.COLOR_RGB2GRAY)

## mode of effects, threshing or erosion
mode = 'thresh'

# gausian thresh  
thresh = cv.adaptiveThreshold(cv_image, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C,cv.THRESH_BINARY, 199, 5)

# using erosion
kernel = numpy.ones((5,5), numpy.uint8) 
img_erosion = cv.erode(cv_image, kernel, iterations=1) 
# img_dilation = cv.dilate(cv_image, kernel, iterations=1) 
# cv.imshow('Input', cv_image) 
# cv.imshow('Erosion', img_erosion) 
# cv.imshow('Dilation', img_dilation) 
# cv.waitKey(0)

# converting cv_image to PIL image back after thresholding

if mode == 'thresh':
	img = cv.cvtColor(thresh, cv.COLOR_GRAY2RGB)
else:
	img = cv.cvtColor(img_erosion, cv.COLOR_GRAY2RGB)
image = Image.fromarray(numpy.array(img))


# inverting color of the image
if mode == "thresh":
	image = ImageOps.invert(image)
image = image.convert('L')

# grabbing box slices from the image for getting each number
box_size = size[0]//9
# making a grid of None's for storing box images
grid = [[None for _ in range(9)] for _ in range(9)]

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
		this = image.crop((left,top,right,bottom))
		twenty = int(box_size*0.2)
		# assigning it to the grid[i][j]
		grid[i][j] = this.crop((twenty,twenty,box_size-twenty, box_size-twenty))

## finding a midpoint to decide borderline whiteness, mid
whites = []
for i in range(9):
	for j in range(9):
		whites.append(whiteness(grid[i][j]))
whites.sort()
tempmax = -1; rindex = None; tsum = sum(whites); leftsum = 0;
for i in range(80):
	leftsum += whites[i]
	rightsum = tsum - leftsum
	avgdiff = rightsum/(81-i+1) - leftsum/(i+1)
	if avgdiff > tempmax:
		tempmax = avgdiff
		rindex = i+1
mid = whites[rindex]-0.05

## making a board for containing potential numbers
board = [[None for _ in range(9)] for _ in range(9)]

## count is a variable made to count the number
## of squares with inputs calculated by this algorithm
count = 0
for i in range(9):
	for j in range(9):
		whites = whiteness(grid[i][j])
		if whites > mid:
			count += 1
		else:
			board[i][j] = 0;
# print(count)

## loading the tensorflow model stored locally
model = models.load_model('weights.h5')

## storing all the results in board array
for i in range(9):
	for j in range(9):
		if board[i][j] == None:
			board[i][j] = recognize(model, grid[i][j])

## printing the damn board
# for i in range(9):
# 	for j in range(9):
# 		print(board[i][j], end = ' ')
# 	print('\n')
