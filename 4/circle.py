import cv2 as cv
import os
import sys
import numpy as np
import math
import random

if __name__ == "__main__":
	in_file = raw_input()
	files = []
	for file in os.listdir(in_file): 
		files.append(file)

	img = cv.imread(os.path.join(in_file,files[0]))
	gray = cv.cvtColor(img,cv.COLOR_BGR2GRAY)

	circles = cv.HoughCircles(gray, cv.HOUGH_GRADIENT,1,20,param1=50,param2=30,minRadius=50,maxRadius=0)
	circles = np.uint16(np.around(circles))
	c = circles[0,0]
	y = c[0]
	x = c[1]
	r = c[2]
	a = [y,x-10]
	b = [y,x-r+10]
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
	cc = aa - bb * 1/5
	dd = aa - bb * 2/5
	ee = aa - bb * 3/5
	ff = aa - bb * 4/5
	w, h, q = img.shape
	center = (y,x)
	counter = 0
	broken = 0
	a = 0
	arcs = []
	arc = 0
	for i in range(0,180):
		M = cv.getRotationMatrix2D(center, 2 , 1.0)
		img = cv.warpAffine(img, M, (w, h))
		pixelA = pixel = img[aa,y]
		pixelB = pixel = img[bb,y]
		pixelC = pixel = img[cc,y]
		pixelD = pixel = img[dd,y]
		pixelE = pixel = img[ee,y]
		pixelF = pixel = img[ff,y]
		if (pixelA[0] > 125 and pixelA[1] > 125 and pixelA[2] > 125 and a == 0) or (pixelB[0] > 125 and pixelB[1] > 125 and pixelB[2] > 125 and a == 0) or (pixelC[0] > 125 and pixelC[1] > 125 and pixelC[2] > 125 and a == 0) or (pixelD[0] > 125 and pixelD[1] > 125 and pixelD[2] > 125 and a == 0) or (pixelE[0] > 125 and pixelE[1] > 125 and pixelE[2] > 125 and a == 0) or (pixelF[0] > 125 and pixelF[1] > 125 and pixelF[2] > 125 and a == 0):
			counter += 1
			# print i,arc
			arc = 2*i - arc
			arcs.append(arc)
			# if (pixelA[0] > 125 and pixelA[1] > 125 and pixelA[2] > 125 and a == 0) and (pixelB[0] > 125 and pixelB[1] > 125 and pixelB[2] > 125 and a == 0):
			# 	broken += 1
			a = 1
		elif not ((pixelA[0] > 125 and pixelA[1] > 125 and pixelA[2] > 125) or (pixelB[0] > 125 and pixelB[1] > 125 and pixelB[2] > 125) or (pixelC[0] > 125 and pixelC[1] > 125 and pixelC[2] > 125) or (pixelD[0] > 125 and pixelD[1] > 125 and pixelD[2] > 125) or (pixelE[0] > 125 and pixelE[1] > 125 and pixelE[2] > 125) or (pixelF[0] > 125 and pixelF[1] > 125 and pixelF[2] > 125) and a == 1):
			if a == 1:
				arc = 2 * i
			a = 0
			# print arc

	arc = max(arcs)
	# print arc

	print str(c[0]), str(c[1]),counter ,0 ,arc ,3 , 21
	# cv.circle(img,(c[0],c[1]),c[2],(0,255,0), 2)
	# cv.circle(img,(c[0],c[1]),1,(0,0,255), 3)
	# cv.imshow("rotated", img)
	# cv.waitKey(0)