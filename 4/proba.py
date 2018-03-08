import cv2 as cv
import os
import sys
import numpy as np
import math

if __name__ == "__main__":
    # in_file = raw_input()
    in_file = 'set/example_4'
    files = []
    for file in os.listdir(in_file): 
        files.append(file)

    img = cv.imread(os.path.join(in_file,files[0]))
    # img = cv.medianBlur(img,5)
    gray = cv.cvtColor(img,cv.COLOR_BGR2GRAY)

    circles = cv.HoughCircles(gray, cv.HOUGH_GRADIENT,1,20,param1=50,param2=30,minRadius=30,maxRadius=0)
    circles = np.uint16(np.around(circles))
    c = circles[0,0]
    print(str(c[0]) + " " + str(c[1]) + " " + str(c[2]))

    #centar i kruznica
    cv.circle(img,(c[0],c[1]),c[2],(0,255,0), 2)
    cv.circle(img,(c[0],c[1]),1,(0,0,255), 3)

    x = c[0]
    y = c[1]
    r = c[2]

    w, h = gray.shape[::-1]
    center = (c[0], c[1])
    print 'center', center
    # imgr = cv.imread(os.path.join(in_file,files[0]))
    for i in range(y - r + 10, y):
        pixel = img[i, x]
        if pixel[0] == 0:
            print(x,y-r+i)         
    # for i in range(0:71):
    #     M = cv.getRotationMatrix2D(center, 5*i, 1.0)
    #     rotated = cv.warpAffine(img, M, (w, h))
    #         pixel2 = imgr[i, j]
    #         if pixel2[0] != 0:
    #             print(pixel2[1])

    # #rotacija
    # M = cv.getRotationMatrix2D(center, 90, 1.0)
    # rotated = cv.warpAffine(img, M, (w, h))

    
    cv.imshow("rotated", img)
    cv.waitKey(0)



    # cv.circle(cimg,(c[0],c[1]),c[2],(0,255,0),2)
    # cv.circle(cimg,(c[0],c[1]),2,(0,0,255),3)
    # cv.imshow('detected circles',cimg)
    # cv.waitKey(0)
    # cv.destroyAllWindows()
