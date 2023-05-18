
import cv2
import numpy as np
import statistics
import os
import matplotlib.pyplot as plt
image = cv2.imread(r'C:\Users\misha\Desktop\diploma\masked_MEL_NV_BCC\ISIC_0024478.jpg')




cv2.imshow('image', image)


height, width, _ = image.shape
print(height, width)

# dir = 'C:/Users/misha/Desktop/diploma/MEL_NV_BCC/'
# with os.scandir(dir) as files:
#     for index, file in enumerate(files, start=1):
#         a = dir + file.name
#         if a[-8:-4] == 'mask':
#             os.remove(a)

flag = 0
point = 100
point2 = 5

if image[int(height/2), int(width - width/64)].sum() < 60 and image[int(height/2), int(width/64)].sum() < 60 and image[int(height/64), int(width/2)].sum() < 60 and image[int(height - height/64), int(width/2)].sum() < 60:
    flag = 1
if flag != 1 and (image[point2, point2].sum() < 450 or image[height - 1 - point2, point2].sum() < 450 or image[point2, width - 1 - point2].sum() < 450 or image[height - 1 - point2, width - 1 - point2].sum() < 450):
    flag = 2

print(flag)
ravel = image.ravel()
n, bins, _ = plt.hist(ravel[ravel > 10], bins=np.linspace(0, 255, 256)) # n - counts
bins = np.delete(bins, 0)
filter_n = n[n > 1000]
quantile = np.quantile(filter_n, 0.2)
tmp_amplitude = bins[n > quantile]

amplitude = tmp_amplitude[len(tmp_amplitude) - 1] - tmp_amplitude[0]
reg = 1
print(amplitude)

if flag == 0:
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (7, 7), 0)

    if 180 < amplitude < 220:
        reg = 2
    elif amplitude <= 180:
        reg = 3

    if reg == 1:
        C = 45
    elif reg == 2:
        C = 35
    else:
        C = -20

    tmp_amplitude_2 = bins[n > np.quantile(filter_n, 0.8)]

    amplitude_2 = tmp_amplitude_2[len(tmp_amplitude_2) - 1] - tmp_amplitude_2[0]
    print(amplitude_2)
    if amplitude_2 < 66 and amplitude <= 180:
        C += 40

    thresh1 = cv2.adaptiveThreshold(blurred, 127, cv2.ADAPTIVE_THRESH_MEAN_C,
                                    cv2.THRESH_BINARY, 1001, C)
    cv2.imshow('Adaptive Mean', thresh1)

    total_mask = thresh1
    total_mask[total_mask == 0] = 255
    cv2.rectangle(total_mask, (0, 0), (width - 1, height - 1), (127, 0, 0), 5)
    cv2.imshow('total_mask', total_mask)

if flag == 2:
    pt1 = int(width / 4)
    for i in range(10, int(width / 4)):
        if image[int(height / 2), i].sum() > 150:
            pt1 = i + 40
            break

    pt2 = int(3 * width / 4)
    for i in range(int(width) - 10, int(3 * width / 4), -1):
        if image[int(height / 2), i].sum() > 150:
            pt2 = i - 40
            break
    if int(width) - pt2 <= pt1:
        radius = (width / 2 - pt1) ** 2
    else:
        radius = (width / 2 - pt2) ** 2
    h = height/2
    w = width/2
    for i in range(height):
        for j in range(width):
            if (i - h) ** 2 + (j - w) ** 2 > radius:
                image[i, j] = 0
    cv2.imshow(',', image)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (7, 7), 0)


    (T, threshInv2) = cv2.threshold(blurred, 10, 255, cv2.THRESH_BINARY)
    cv2.imshow("Threshold2", threshInv2)


    masked = cv2.bitwise_and(image, image, mask=threshInv2)
    cv2.imshow("Output2", masked)

    image_copy = masked.copy()
    gray = cv2.cvtColor(image_copy, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (7, 7), 0)

    tmp_amplitude_2 = bins[n > np.quantile(filter_n, 0.8)]

    amplitude_2 = tmp_amplitude_2[len(tmp_amplitude_2) - 1] - tmp_amplitude_2[0]
    print(amplitude_2)

    if 80 < amplitude < 230:
        reg = 2
    elif amplitude >= 230:
        reg = 3
    if reg == 1:
        C = -65
    elif reg == 2:
        C = -45
    else:
        C = -5

    print(pt1, pt2, width - 60)
    if pt1 < 60 and pt2 > width - 60 and 200 > amplitude > 110:
        C += 30
    if pt1 > 130 and pt2 < width - 130 and 200 > amplitude > 110:
        C -= 30
    if pt1 > 160 and pt2 < width - 160 and amplitude >= 200:
        C -= 65


    thresh1 = cv2.adaptiveThreshold(blurred, 127, cv2.ADAPTIVE_THRESH_MEAN_C,
                                    cv2.THRESH_BINARY, 1001, C)



    cv2.imshow('Adaptive Mean', thresh1)

    skin = image
    skin[thresh1 == 127] = 127
    cv2.imshow('skin', skin)

    lesion = skin
    contours, hierarchy = cv2.findContours(image=threshInv2, mode=cv2.RETR_TREE, method=cv2.CHAIN_APPROX_NONE)

    cv2.drawContours(image=threshInv2, contours=contours, contourIdx=-1, color=(0, 0, 0), thickness=5,
                     lineType=cv2.LINE_AA)


    cv2.imshow('wtwet', threshInv2)

    lesion[threshInv2 == 0] = 0
    lesion = cv2.cvtColor(lesion, cv2.COLOR_BGR2GRAY)
    lesion[np.logical_and(lesion != 0, thresh1 != 127)] = 255


    cv2.imshow('total_mask', lesion)


if flag == 1:
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (7, 7), 0)

    (T, threshInv2) = cv2.threshold(blurred, 10, 255, cv2.THRESH_BINARY)
    cv2.imshow("Threshold2", threshInv2)


    masked = cv2.bitwise_and(image, image, mask=threshInv2)
    cv2.imshow("Output2", masked)


    image_copy = masked.copy()
    gray = cv2.cvtColor(image_copy, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (7, 7), 0)

    if amplitude > 200:
        reg = 2

    if reg == 1:
        C = 5
    else:
        C = -20

    thresh1 = cv2.adaptiveThreshold(blurred, 127, cv2.ADAPTIVE_THRESH_MEAN_C,
                                    cv2.THRESH_BINARY, 441, C)



    cv2.imshow('Adaptive Mean', thresh1)

    skin = image
    skin[thresh1 == 127] = 127
    cv2.imshow('skin', skin)

    lesion = skin



    contours, hierarchy = cv2.findContours(image=threshInv2, mode=cv2.RETR_TREE, method=cv2.CHAIN_APPROX_NONE)


    cv2.drawContours(image=threshInv2, contours=contours, contourIdx=-1, color=(0, 0, 0), thickness=75,
                     lineType=cv2.LINE_AA)


    lesion[threshInv2 == 0] = 0
    lesion = cv2.cvtColor(lesion, cv2.COLOR_BGR2GRAY)
    lesion[np.logical_and(lesion != 0, thresh1 != 127)] = 255
    cv2.imshow('total_mask', lesion)


if cv2.waitKey(0) & 0xff == 27:
    cv2.destroyAllWindows()




