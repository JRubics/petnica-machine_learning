import cv2 as cv
import numpy as np
import math

h_yellow_l = 20
s_yellow_l = 120
v_yellow_l = 130
h_yellow_h = 30
s_yellow_h = 255
v_yellow_h = 255

h_gold_l = 10
s_gold_l = 160
v_gold_l = 80
h_gold_h = 22
s_gold_h = 230
v_gold_h = 129

h_orange_l = 3
s_orange_l = 170
v_orange_l = 180
h_orange_h = 19
s_orange_h = 255
v_orange_h = 255

h_purple_l = 140
s_purple_l = 105
v_purple_l = 20
h_purple_h = 173
s_purple_h = 210
v_purple_h = 150

h_green_l = 45
s_green_l = 90
v_green_l = 30
h_green_h = 80
s_green_h = 255
v_green_h = 210

h_blue_l = 81
s_blue_l = 48
v_blue_l = 50
h_blue_h = 120
s_blue_h = 255
v_blue_h = 255

h_brown_l = 3
s_brown_l = 180
v_brown_l = 100
h_brown_h = 65
s_brown_h = 255
v_brown_h = 150

h_gray_l = 0
s_gray_l = 0
v_gray_l = 30
h_gray_h = 100
s_gray_h = 20
v_gray_h = 220

h_red_l = 0
s_red_l = 130
v_red_l = 100
h_red_h = 5
s_red_h = 255
v_red_h = 255

h_white_l = 0
s_white_l = 0
v_white_l = 200
h_white_h = 180
s_white_h = 20
v_white_h = 255

h_black_l = 0
s_black_l = 0
v_black_l = 0
h_black_h = 180
s_black_h = 8
v_black_h = 30

color_dict = {
	'black' : 0,
	'white' : 0,
	'red' : 0,
	'orange' : 0,
	'gray' : 0,
	'blue' : 0,
	'brown' : 0,
	'gold' : 0,
	'green' : 0,
	'purple' : 0,
	'yellow' : 0,
}

def main():
	filename = raw_input()
	# for i in range(1,11):
	# filename = "set/A" + str(i) +".png"
	src = cv.imread(filename)
	w, h, c = src.shape

	# cv.imshow("a",src)
	# cv.waitKey()

	# hsv = cv.cvtColor(src,cv.COLOR_BGR2HSV)
	lower_rose = np.array([165,40,200])
	upper_rose = np.array([180,170,255])
	# mask = cv.inRange(hsv, lower_rose, upper_rose)
	# res = cv.bitwise_and(src,src, mask= mask)

	
	# cv.imshow('res',src)
	# cv.waitKey()

	ha = 0
	s = 0
	v = 0
	k = 0
	hsv = cv.cvtColor(src,cv.COLOR_BGR2HSV)
	for i in range(0,w,20):
		for j in range(0,h,20):
			pixel = hsv[i,j]
			ha +=pixel[0]
			s +=pixel[1]
			v +=pixel[2]
			k += 1
	ha /= k
	s /= k
	v /= k
	if ha > lower_rose[0] and ha < upper_rose[0] and s > lower_rose[1] and s < upper_rose[1] and v > lower_rose[2] and v < upper_rose[2]:
		# hsv = cv.cvtColor(src,cv.COLOR_BGR2HSV)
		# lower_rose = np.array([165,0,160])
		# upper_rose = np.array([180,170,255])
		# print "ROXA"
		mask = cv.inRange(hsv, lower_rose, upper_rose)
		res = cv.bitwise_not(src,src, mask= mask)
		res = cv.bitwise_and(src,src, mask= mask)
		# src = cv.cvtColor(res,cv.COLOR_HSV2BGR)


	resize_coeff = 0.4
	src = cv.resize(src, (int(resize_coeff * h), int(resize_coeff * w)))		

	img = cv.cvtColor(src, cv.COLOR_BGR2GRAY)
	img = cv.medianBlur(img, 7)
	img = cv.Canny(img, 100, 200)

	kernel = np.ones((5, 5), np.uint8)
	img = cv.dilate(img, kernel, 1)
	img = cv.erode(img, kernel, 1)

	img, contours, hierarchy = cv.findContours(img, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

	if len(contours) is not 0:
		max_index, max_area = max(enumerate([cv.contourArea(x) for x in contours]), key = lambda x: x[1])
		max_contour = contours[max_index]

		rect = cv.minAreaRect(max_contour)
		box = cv.boxPoints(rect)

		if box[0,0] < 0 or box[0,1] < 0 or box[1,0] < 0 or box[1,1] < 0 or box[2,0] < 0 or box[2,1] < 0 or box[3,0] < 0 or box[3,1] < 0:
			return "111G"
		box = sortByX(box)

		center = ((box[0,0] + box[1,0] + box[2,0] + box[3,0])/4,(box[0,1] + box[1,1] + box[2,1] + box[3,1])/4)

		x = abs(box[0,0] - box[2,0])
		y = abs(box[0,1] - box[2,1])	
		alpha = np.arctan2(y,x)
		if box[0,1] < box[2,1]:
			alpha = -alpha
		box = rotate(box,-alpha,center)
		M = cv.getRotationMatrix2D(center, np.degrees(alpha) , 1.0)
		src = cv.warpAffine(src, M, (int(h*2), int(w*2)))
		box = np.int0(box)
		box = sortByX(box)

		#crop
		src = src[box[1,1]+6:box[0,1]-6,box[2,0]+6:box[0,0]-6]
		if len(src) is 0:
			return "111G"
		
		img = RGBimage(src)
		colors = findColors(img)

		colors = removeColors(colors)
		# print colors
		printColors(colors)
		# cv.imshow("rgb", img)
		# cv.waitKey()

def printColors(colors):
	colors1 = []
	for i in range(0,len(colors)):
		if colors1.__contains__(colors[i]):
			if colors[i-1] != colors[i]:
				colors1.append(colors[i])
			elif countColor(colors,i) > 3 and countColor(colors,i) < 7 and colors1.count(colors[i]) == 1:
				colors1.append(colors[i])
			elif countColor(colors,i) >= 7 and countColor(colors,i) == 2:
				colors1.append(colors[i])
				colors1.append(colors[i])
		else:
			colors1.append(colors[i])
	colors1 = colors1[0:3]
	k = 0
	while len(colors1) <= 2:
		colors1.append("gold")
	# print k
	colors1.append("gold")
	s = ""
	for color in colors1:
		if color == "black":
			s += '0'
		elif color == "brown":
			s += '1'
		elif color == "red":
			s += '2'
		elif color == "orange":
			s += '3'
		elif color == "yellow":
			s += '4'
		elif color == "green":
			s += '5'
		elif color == "blue":
			s += '6'
		elif color == "purple":
			s += '7'
		elif color == "gray":
			s += '8'
		elif color == "white":
			s += '9'
		elif color == "gold":
			s += 'G'
	print s

def countColor(colors,i):
	k = 1
	color = colors[i]
	for j in range (i+1,len(colors)):
		if colors[j] == color:
			k += 1;
		else:
			return k
	return k
		

def removeColors(colors):
	colors1 = []
	for i in range(1,len(colors)):
		if colors[i-1] == "brown" and colors[i] == "yellow":
			colors[i] = colors[i-1]
		elif colors[i] == "brown" and colors[i-1] == "yellow":
			colors[i] = colors[i-1]
	if colors[0] == colors[1]:
		colors1.append(colors[0])
	for i in range(1,len(colors)-1):
		if colors[i] == colors[i+1] or colors[i] == colors[i-1]:
			colors1.append(colors[i])
	if colors[len(colors)-2] == colors[len(colors)-1]:
		colors1.append(colors[len(colors)-1])
	return colors1

def findColors(img):
	colors = []
	hsv = cv.cvtColor(img,cv.COLOR_BGR2HSV);
	h, w, c = hsv.shape
	for i in range(0,w):
		h = hsv[0,i,0]
		s = hsv[0,i,1]
		v = hsv[0,i,2]
		# print i, h,s,v
		if h <= h_black_h and h >= h_black_l and s <= s_black_h and s >= s_black_l and v <= v_black_h and v >= v_black_l:
			colors.append("black")
		elif h <= h_yellow_h and h >= h_yellow_l and s <= s_yellow_h and s >= s_yellow_l and v <= v_yellow_h and v >= v_yellow_l:
			colors.append("yellow")
		elif h <= h_blue_h and h >= h_blue_l and s <= s_blue_h and s >= s_blue_l and v <= v_blue_h and v >= v_blue_l:
			colors.append("blue")
		elif h <= h_red_h and h >= h_red_l and s <= s_red_h and s >= s_red_l and v <= v_red_h and v >= v_red_l:
			colors.append("red")
		elif h <= h_green_h and h >= h_green_l and s <= s_green_h and s >= s_green_l and v <= v_green_h and v >= v_green_l:
			colors.append("green")
		elif h <= h_purple_h and h >= h_purple_l and s <= s_purple_h and s >= s_purple_l and v <= v_purple_h and v >= v_purple_l:
			colors.append("purple")
		elif h <= h_gold_h and h >= h_gold_l and s <= s_gold_h and s >= s_gold_l and v <= v_gold_h and v >= v_gold_l:
			colors.append("gold")
		elif h <= h_gray_h and h >= h_gray_l and s <= s_gray_h and s >= s_gray_l and v < v_gray_h and v >= v_gray_l:
			colors.append("gray")
		elif h <= h_brown_h and h >= h_brown_l and s <= s_brown_h and s >= s_brown_l and v <= v_brown_h and v >= v_brown_l:
			colors.append("brown")
		elif h <= h_white_h and h >= h_white_l and s <= s_white_h and s >= s_white_l and v <= v_white_h and v >= v_white_l:
			colors.append("white")
		elif h <= h_orange_h and h >= h_orange_l and s <= s_orange_h and s >= s_orange_l and v <= v_orange_h and v >= v_orange_l:
			colors.append("orange")
		else :
			continue
	return colors

def RGBimage(src):
	h, w, c = src.shape
	img = np.zeros((1,w,3),np.uint8)
	for i in range(0,w):
		r = 0
		g = 0
		b = 0
		for j in range(0,h):
			r+=src[j,i,2]
			g+=src[j,i,1]
			b+=src[j,i,0]
		r /= h
		g /= h
		b /= h
		img[0,i,0] = b
		img[0,i,1] = g
		img[0,i,2] = r 
	return img

def rotate(box,alpha,center):
	cos = np.cos(alpha)
	sin = np.sin(alpha)
	for i in range(0,4):
		box[i,0] -= center[0]
		box[i,1] -= center[1]
		x = box[i,0] * cos - box[i,1] * sin
		y = box[i,0] * sin + box[i,1] * cos
		box[i,0] = x + center[0]
		box[i,1] = y + center[1]
	return box
		

def sortByX(box):
	for i in range(0,3):
		for j in range(i,4):
			if box[i,0] < box[j,0] or (box[i,0] == box[j,0] and box[i,1] < box[j,1]):
				box[i,0], box[j,0] = box[j,0], box[i,0]
				box[i,1], box[j,1] = box[j,1], box[i,1]
	return box

if __name__ == "__main__":
	main()
