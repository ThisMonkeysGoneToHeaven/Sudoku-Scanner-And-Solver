# loading necessary libraries
import sys
import numpy
import cv2 as cv
from PIL import Image, ImageOps

def checkempty(pic):
	total_pixels = pic.size[0]*pic.size[1]
	# white_pixels = numpy.sum(numpy.array(pic)==255)
	white_pixels = numpy.sum(numpy.array(pic) > 185)
	return (white_pixels/total_pixels)

# loading the image
image = Image.open('image2.jpg').convert('RGB')

# resizing image upto a Good size
size = (400,400)
image = image.resize(size)

## applying adaptive thresholding using opencv
cv_image = cv.cvtColor(numpy.array(image), cv.COLOR_RGB2GRAY)
# gausian thresh  
thresh = cv.adaptiveThreshold(cv_image, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C,cv.THRESH_BINARY, 199, 5)

# kernel = numpy.ones((5,5), numpy.uint8) 
# img_erosion = cv.erode(cv_image, kernel, iterations=1) 
# img_dilation = cv.dilate(cv_image, kernel, iterations=1) 
# cv.imshow('Input', cv_image) 
# cv.imshow('Erosion', img_erosion) 
# cv.imshow('Dilation', img_dilation) 
# cv.waitKey(0)

# converting cv_image to PIL image back after thresholding
img = cv.cvtColor(thresh, cv.COLOR_BGR2RGB)
image = Image.fromarray(numpy.array(img))


# inverting color of the image
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
		ten = int(box_size*0.1)
		fifteen = int(box_size*0.15)
		tfour = int(box_size*0.24)
		# assigning it to the grid[i][j]
		grid[i][j] = this.crop((tfour,ten,box_size-fifteen, box_size-fifteen))

# # count = 0
# for i in range(9):
# 	for j in range(9):
# 		white = checkempty(grid[i][j])
# 		grid[i][j].show()
# 		print(white)
# 		a  = input()
# 		# if white < .09:
# 		# 	count += 1
# # print(count)
image.show()