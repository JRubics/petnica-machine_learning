import cv2

img = cv2.imread("A9.png")
crop_img = img[5:55, 5:25]
cv2.imshow("cropped", crop_img)
cv2.waitKey(0)