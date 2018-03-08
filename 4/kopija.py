import cv2 as cv
import os
import sys
import numpy as np
import math

if __name__ == "__main__":
	# for i in range(1,11):
	in_file = raw_input()
		# in_file = "set/example_" + str(i)
	files = []
	for file in os.listdir(in_file): 
		files.append(file)

	img = cv.imread(os.path.join(in_file,files[0]))
	gray = cv.cvtColor(img,cv.COLOR_BGR2GRAY)

	circles = cv.HoughCircles(gray, cv.HOUGH_GRADIENT,1,20,param1=50,param2=30,minRadius=50,maxRadius=0)
	circles = np.uint16(np.around(circles))
	c = circles[0,0]

	#2
	y = c[0]
	x = c[1]
	r = c[2]
	a = [y,x-10]
	b = [y,x-r+10]
	# print a,b
	aa = a[1]
	bb = b[1]
	for i in range(bb,aa):
		pixel = img[i,x]
		if pixel[0] != 0 and pixel[1] != 0 and pixel[2] != 0:
			b[1] += 1
		else: break
	for i in range(bb,aa):
		pixel = img[aa-i,x]
		if pixel[0] != 0 and pixel[1] != 0 and pixel[2] != 0:
			a[1] -= 1
		else: break
	aa = a[1] - 30
	bb = b[1] + 30

	w, h, q = img.shape
	center = (y,x)
	counter = 0
	broken = 0
	a = 0
	for i in range(0,60):
		M = cv.getRotationMatrix2D(center, 6 , 1.0)
		img = cv.warpAffine(img, M, (w, h))
		pixelA = pixel = img[aa,y]
		pixelB = pixel = img[bb,y]
		if (pixelA[0] > 125 and pixelA[1] > 125 and pixelA[2] > 125 and a == 0) or (pixelB[0] > 125 and pixelB[1] > 125 and pixelB[2] > 125 and a == 0):
			counter += 1
			if (pixelA[0] > 125 and pixelA[1] > 125 and pixelA[2] > 125 and a == 0) and (pixelB[0] > 125 and pixelB[1] > 125 and pixelB[2] > 125 and a == 0):
				broken += 1
			a = 1
		elif not ((pixelA[0] > 125 and pixelA[1] > 125 and pixelA[2] > 125) or (pixelB[0] > 125 and pixelB[1] > 125 and pixelB[2] > 125) and a == 1):
			a = 0

	print str(c[0]), str(c[1]),counter ,counter - broken ,0 ,0 ,0
	cv.circle(img,(c[0],c[1]),c[2],(0,255,0), 2)
	cv.circle(img,(c[0],c[1]),1,(0,0,255), 3)
	cv.imshow("rotated", img)
	cv.waitKey(0)