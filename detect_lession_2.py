# Python program to illustrate
# adaptive thresholding type on an image

# organizing imports
import cv2
import numpy as np
import random
# path to input image is specified and
# image is loaded with imread command
image1 = cv2.imread(r'C:\Users\misha\Desktop\diploma\images\ISIC_0000036_downsampled.jpg')
image = cv2.imread(r'C:\Users\misha\Desktop\diploma\images\ISIC_0000036_downsampled.jpg')

cv2.imshow('image', image1)
height, width, _ = image1.shape
flag = 0
point = 100
point2 = 5
if image1[point, point].sum() < 100 or image1[height - 1 - point, point].sum() < 100 or image1[point, width - 1 - point].sum() < 100 or image1[height - 1 - point, width - 1 - point].sum() < 100:
    flag = 1
if flag != 1 and (image[point2, point2].sum() < 170 or image[height - 1 - point2, point2].sum() < 170 or image[point2, width - 1 - point2].sum() < 170 or image[height - 1 - point2, width - 1 - point2].sum() < 170):
    flag = 2
print(flag)
print(image[point2, point2], image[height - 1 - point2, point2], image[point2, width - 1 - point2], image[height - 1 - point2, width - 1 - point2])

gray = cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY)
blurred = cv2.GaussianBlur(gray, (7, 7), 0)
#(T, threshInv) = cv2.threshold(blurred, 0, 255, cv2.THRESH_OTSU)  #этот хуже работает
(T, threshInv2) = cv2.threshold(blurred, 10, 255, cv2.THRESH_BINARY)
cv2.imshow("Threshold2", threshInv2)
#cv2.imshow("Threshold", threshInv)
cv2.imshow("Threshold2,cot", threshInv2)
#masked = cv2.bitwise_and(image1, image, mask=threshInv)
#cv2.imshow("Output", masked)
masked = cv2.bitwise_and(image1, image, mask=threshInv2)
cv2.imshow("Output2", masked)


image_copy = masked.copy()
gray = cv2.cvtColor(image_copy, cv2.COLOR_BGR2GRAY)
blurred = cv2.GaussianBlur(gray, (7, 7), 0)

########################
# applying different thresholding
# techniques on the input image

thresh1 = cv2.adaptiveThreshold(blurred, 127, cv2.ADAPTIVE_THRESH_MEAN_C,
                                cv2.THRESH_BINARY, 441, -10)



cv2.imshow('Adaptive Mean', thresh1)

skin = image1
skin[thresh1 == 127] = 127
cv2.imshow('skin', skin)

lesion = skin
contours, hierarchy = cv2.findContours(image=threshInv2, mode=cv2.RETR_TREE, method=cv2.CHAIN_APPROX_NONE)


cv2.drawContours(image=threshInv2, contours=contours, contourIdx=-1, color=(0, 0, 0), thickness=55,
                 lineType=cv2.LINE_AA)
lesion[threshInv2 == 0] = 0
lesion = cv2.cvtColor(lesion, cv2.COLOR_BGR2GRAY)
cv2.imshow('lessib_gra', lesion)
lesion[np.logical_and(lesion > 0, thresh1 != 127)] = 255

cv2.imshow('lesion', lesion)

mask_skin = thresh1
mask_skin[mask_skin == 127] = 255
skin = cv2.bitwise_and(image, image, mask=mask_skin)
mask_lesion = lesion
mask_lesion[mask_skin == 255] = 0
#mask_lesion = cv2.bitwise_not(mask_lesion)
lesion = cv2.bitwise_and(image, image, mask=mask_lesion)

cv2.imshow('mask_lesion', lesion)
cv2.imshow('mask_skin', skin)

# skin = image1
# skin[thresh1 == 127] = 127
# cv2.imshow('skin', skin)
#
# lesion = skin
# lesion[skin == 127] = 0
# contours, hierarchy = cv2.findContours(image=threshInv2, mode=cv2.RETR_TREE, method=cv2.CHAIN_APPROX_NONE)
#
#
# cv2.drawContours(image=threshInv2, contours=contours, contourIdx=-1, color=(0, 0, 0), thickness=25,
#                  lineType=cv2.LINE_AA)
# lesion[threshInv2 == 0] = 0
# lesion[lesion > 0] = 127
# cv2.imshow('lesion', lesion)

if cv2.waitKey(0) & 0xff == 27:
    cv2.destroyAllWindows()



