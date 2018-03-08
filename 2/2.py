import cv2 as cv
import os
import sys
import numpy as np
import math

def findC(xx,xy,yx,yy,x,y):
    fix = np.arctan2(xy,xx)
    fiy = np.arctan2(yy,yx)
    fiC = np.arctan2(y,x)
    fiC -= fix
    yny = round(math.sqrt(yx * yx + yy * yy) * np.sin(fiy - fix),2)
    r = math.sqrt(x * x + y * y)
    x = r * np.cos(fiC)
    y = r * np.sin(fiC)
    if yny < 0:
        y *= -1
    return [x,y]

if __name__ == "__main__":
    in_file = raw_input()
    files = []
    for subdir in os.listdir(in_file): 
        for file in os.listdir(os.path.join(in_file,subdir)):
            files.append(os.path.join(subdir,file))
    files.sort()
    for file in files:
        with open(os.path.join(in_file,file), "r") as f:
            i = 0
            for line in f:
                numbers = line.split()
                numbers = [ float(x) for x in numbers ]
                [x,y] = findC(numbers[2]-numbers[0],numbers[3]-numbers[1],numbers[4]-numbers[0],numbers[5]-numbers[1],numbers[6]-numbers[0],numbers[7]-numbers[1])
                print(file + " " + str(i) + " " + str(round(x,4)) + " " + str(round(y,4)))
                i += 1



                    