# Python program to illustrate
# adaptive thresholding type on an image

# organizing imports 
import cv2
import numpy as np
import random
# path to input image is specified and  
# image is loaded with imread command 
image1 = cv2.imread(r'C:\Users\misha\Desktop\diploma\hand_images\ISIC_0000393_downsampled.jpg')
image = cv2.imread(r'C:\Users\misha\Desktop\diploma\hand_images\ISIC_0000393_downsampled.jpg')
image_copy = image1.copy()
black_pixel = 0
height, width, _ = image1.shape

for i in range(height):
    for j in range(width):
        # img[i, j] is the RGB pixel at position (i, j)
        # check if it's [0, 0, 0] and replace with [255, 255, 255] if so
        if image1[i, j].sum() < 170 and (i - height / 2) ** 2 + (j - width / 2) ** 2 > (height / 2) ** 2 - 15000:
            black_pixel += 1
            image1[i, j] = [-1, -1, -1]
print(black_pixel)
# print(image1)
# cv2.cvtColor is applied over the
# image input with applied parameters
# to convert the image in grayscale 
img = cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY)

img = cv2.GaussianBlur(img, (7, 7), 0)

# ret, thresh0 = cv2.threshold(img, 150, 255, cv2.THRESH_BINARY)
#######################################
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
blurred = cv2.GaussianBlur(gray, (7, 7), 0)
(T, threshInv) = cv2.threshold(blurred, 0, 255, cv2.THRESH_OTSU)
cv2.imshow("Threshold", threshInv)
print("[INFO] otsu's thresholding value: {}".format(T))
# visualize only the masked regions in the image
masked = cv2.bitwise_and(image, image, mask=threshInv)
cv2.imshow("Output", masked)
########################
# applying different thresholding 
# techniques on the input image
thresh1 = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_MEAN_C,
                                cv2.THRESH_BINARY, 1001, 35)

thresh2 = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                cv2.THRESH_BINARY, 1001, 25)

# height, width = thresh1.shape
#
# for i in range(height):
#     for j in range(width):
#         # img[i, j] is the RGB pixel at position (i, j)
#         # check if it's [0, 0, 0] and replace with [255, 255, 255] if so
#         if (i-height/2)**2 + (j-width/2)**2 > (height/2)**2 - 20000:
#             thresh1[i, j] = 255
# print(thresh1)

# the window showing output images
# with the corresponding thresholding 
# techniques applied to the input image
# cv2.imshow('bin', thresh0)
cv2.imshow('Adaptive Mean', thresh1)
# cv2.imshow('Adaptive Gaussian', thresh2)
cv2.imshow('image', image1)


skin = image1
skin[thresh1 == 255] = 0
cv2.imshow('skin', skin)

height, width = thresh1.shape

if black_pixel > 2000:
    print('lol')
    for i in range(height):
        for j in range(width):
            # img[i, j] is the RGB pixel at position (i, j)
            # check if it's [0, 0, 0] and replace with [255, 255, 255] if so
            if thresh1[i, j].sum() < 120 and (i - height / 2) ** 2 + (j - width / 2) ** 2 > (height / 2) ** 2 - 15000:
                thresh1[i, j] = 255

cv2.imshow('total mask', thresh1)

# поиск центра масс
count = 0
count_x = 0
count_y = 0
print(thresh1)
for x in range(width):
    for y in range(height):
        if thresh1[y][x] == 0:
            count += 1
            count_x += x
            count_y += y
center_x = count_x / count
center_y = count_y / count

# print(img)
# img[thresh1 == 255] = 0
# print(img)
img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)



contours, hierarchy = cv2.findContours(image=thresh1, mode=cv2.RETR_TREE, method=cv2.CHAIN_APPROX_NONE)

# рисуем контуры на исходном изображении

cv2.drawContours(image=image_copy, contours=contours, contourIdx=-1, color=(0, 255, 0), thickness=2,
                 lineType=cv2.LINE_AA)

cv2.circle(image_copy, (int(center_x), int(center_y)), 10, (255, 0, 0), -1)

height, width = thresh1.shape

radius1 = height-center_y
radius2 = center_y
radius3 = width-center_x
radius4 = center_x
radiuses = [radius1, radius2, radius3, radius4]

radius = height + width
for rad in radiuses:
    if radius > rad:
        radius = rad

coef = 0.7 # подумать насчет радиуса выделенной области

point1 = (int(center_x), int(center_y + radius * coef))
point2 = (int(center_x), int(center_y - radius * coef))
point3 = (int(center_x + radius * coef * np.sin(np.pi / 3)), int(center_y - radius * coef * np.cos(np.pi / 3)))
point4 = (int(center_x - radius * coef * np.sin(np.pi / 3)), int(center_y - radius * coef * np.cos(np.pi / 3)))
point5 = (int(center_x + radius * coef * np.sin(np.pi / 3)), int(center_y + radius * coef * np.cos(np.pi / 3)))
point6 = (int(center_x - radius * coef * np.sin(np.pi / 3)), int(center_y + radius * coef * np.cos(np.pi / 3)))

points = [point1, point2, point3, point4, point5, point6]


if radius * 0.2 > 70:
    diag = 70
else:
    diag = int(radius * 0.2)
print(radius * 0.2)
print(diag)


for point in points:
    cv2.circle(image_copy, point, 10, (255, 0, 0), -1)
    cv2.rectangle(image_copy, (point[0] - diag, point[1] + diag), (point[0] + diag, point[1] - diag), (0, 0, 255), 3)
    temp_rectangle = thresh1[point[1] - diag:point[1] + diag, point[0] - diag:point[0] + diag]  # y:y+height, x:x+width
    temp_height, temp_width = temp_rectangle.shape
    black_count = 0
    all_count = 0
    for i in range(temp_height):
        for j in range(temp_width):
            if temp_rectangle[i, j] == 0:
                black_count += 1
            all_count += 1
    if all_count != 0:
        print(black_count / all_count)

tmp = 0
tmp_index = 0
for index, i in enumerate(contours):
    if len(i) > tmp and i[0][0][0] != 0 and i[0][0][1] != 0:
        tmp = len(i) - 1
        tmp_index = index
a = 5
print('\n', '_______________________')
for i in range(7):
    if i == 6:
        break
    point = contours[tmp_index][random.randint(int(tmp/7 * i), int(tmp/7 * (i + 1)))]
    point = (point[0][0], point[0][1])
    a += 1
    cv2.circle(image_copy, point, a, (0, 0, 0), -1)
    cv2.rectangle(image_copy, (point[0] - diag, point[1] + diag), (point[0] + diag, point[1] - diag), (0, 0, 255), 3)
    temp_rectangle = thresh1[point[1] - diag:point[1] + diag, point[0] - diag:point[0] + diag]  # y:y+height, x:x+width
    temp_height, temp_width = temp_rectangle.shape
    black_count = 0
    all_count = 0
    for i in range(temp_height):
        for j in range(temp_width):
            if temp_rectangle[i, j] == 0:
                black_count += 1
            all_count += 1
    if all_count != 0:
        print(black_count / all_count)


#cv2.imshow('temp', temp_rectangle)
# смотрим результаты
cv2.imshow('None approximation', image_copy)
# cv2.imwrite('contours_none_image1.jpg', image_copy)


if cv2.waitKey(0) & 0xff == 27:
    cv2.destroyAllWindows()
