import cv2
import os
from datetime import datetime


def take_mask(path):  # r'C:\Users\misha\Desktop\diploma\images\ISIC_0000000.jpg'
    image1 = cv2.imread(path)

    black_pixel = 0
    height, width, _ = image1.shape
    for i in range(height):
        for j in range(width):
            if image1[i, j].sum() < 170 and (i - height / 2) ** 2 + (j - width / 2) ** 2 > (height / 2) ** 2 - 15000:
                black_pixel += 1
                image1[i, j] = [-1, -1, -1]
    img = cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY)
    img = cv2.GaussianBlur(img, (7, 7), 0)

    thresh1 = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_MEAN_C,
                                    cv2.THRESH_BINARY, 1001, 35)

    path0 = path[:-4] + '_adaptive' + path[-4:]
    cv2.imwrite(path0, thresh1)

    height, width = thresh1.shape
    if black_pixel > 2000:
        for i in range(height):
            for j in range(width):
                # img[i, j] is the RGB pixel at position (i, j)
                # check if it's [0, 0, 0] and replace with [255, 255, 255] if so
                if thresh1[i, j].sum() < 120 and (i - height / 2) ** 2 + (j - width / 2) ** 2 > (
                        height / 2) ** 2 - 15000:
                    thresh1[i, j] = 255

    path = path[:-4] + '_mask' + path[-4:]
    cv2.imwrite(path, thresh1)



dir = 'C:/Users/misha/Desktop/diploma/MEL_images/'


with os.scandir(dir) as files:
    start_time = datetime.now()
    print(start_time)
    for index, file in enumerate(files, start=1):
        take_mask(dir + file.name)
        if index % 10 == 0:
            print(index)
            print(datetime.now() - start_time)

print(datetime.now() - start_time)
