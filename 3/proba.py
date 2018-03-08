import cv2
import numpy as np
from matplotlib import pyplot as plt

images = ['set/A1.png','set/A2.png','set/A3.png','set/A4.png','set/A5.png','set/A6.png','set/A7.png','set/A8.png','set/A9.png','set/A10.png']
img = cv2.imread(images[7],0)
img2 = img.copy()
template = cv2.imread('A9.png',0)
w, h = template.shape[::-1]

# All the 6 methods for comparison in a list
meth = 'cv2.TM_CCOEFF'


def rotateImage(image, angle):
  image_center = tuple(np.array(image.shape)/2)
  rot_mat = cv2.getRotationMatrix2D(image_center,angle,1.0)
  result = cv2.warpAffine(image, rot_mat, image.shape,flags=cv2.INTER_LINEAR)
  return result

if __name__ == "__main__":

    img = cv2.imread(images[6])
    pixel1 = img[1, 1]
    pixel2 = img[20, 630]
    pixel3 = img[470, 10]
    pixel4 = img[470, 630]
    avgR = (int(pixel1[2]) + int(pixel2[2]) + int(pixel3[2]) + int(pixel4[2])) / 4 
    avgG = (int(pixel1[1]) + int(pixel2[1]) + int(pixel3[1]) + int(pixel4[1])) / 4
    avgB = (int(pixel1[0]) + int(pixel2[0]) + int(pixel3[0]) + int(pixel4[0])) / 4
    print(avgR,avgG,avgB)
    for i in range(0,469):
        for j in range(0,639):
            pixel = img[i,j]
            if (pixel[0] < avgB-10 or pixel[0] > avgB+10) and (pixel[1] < avgG-10 or pixel[1] > avgG+10) and (pixel[2] < avgR-10 or pixel[2] > avgR+10):
                img[i,j] = [0,0,0]
    cv2.imshow("rotated", img)
    cv2.waitKey(0)
    # center = (w / 2, h / 2)
    # # rotate the image by 180 degrees
    # M = cv2.getRotationMatrix2D(center, 20, 1.0)
    # rotated = cv2.warpAffine(template, M, (w, h))
    # cv2.imshow("rotated", rotated)
    # cv2.waitKey(0)

    # for x in range(0,12):
    #     M = cv2.getRotationMatrix2D(center, 30*x, 1.0)
    #     template = cv2.warpAffine(template, M, (w, h))
    # for i in range(0,len(images)):
    #     img = cv2.imread(images[i],0)
    #     method = eval(meth)

    #     # Apply template Matching
    #     res = cv2.matchTemplate(img,template,method)
    #     min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

    #     # If the method is TM_SQDIFF or TM_SQDIFF_NORMED, take minimum
    #     if method in [cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED]:
    #         top_left = min_loc
    #     else:
    #         top_left = max_loc
    #     bottom_right = (top_left[0] + w, top_left[1] + h)

    #     cv2.rectangle(img,top_left, bottom_right, 255, 2)

    #     plt.subplot(121),plt.imshow(res,cmap = 'gray')
    #     plt.title('Matching Result'), plt.xticks([]), plt.yticks([])
    #     plt.subplot(122),plt.imshow(img,cmap = 'jet')
    #     plt.title('Detected Point'), plt.xticks([]), plt.yticks([])
    #     plt.suptitle(meth)

    #     plt.show()