import cv2
import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt
import shutil
import os
import sys

# global res
# res = []
# def clean_data(dir, file_name):
#     if file_name[-5] != 'k':
#         return 0
#     global res
#     image = cv2.imread(dir + file_name, cv2.IMREAD_GRAYSCALE)
#     gray = len(image[np.logical_and(50 < image, image < 150)])
#     black = len(image[image <= 50])
#     white = len(image[image >= 150])
#     if black > 0:
#         if white < 0.05 * gray or white > 1.7 * gray:
#             res.append(file_name)
#             # print('gray', gray)
#             # print('black', black)
#             # print('white', white)
#     else:
#         if white < 0.01 * gray or white > 2 * gray:
#             res.append(file_name)
#             # print('gray', gray)
#             # print('black', black)
#             # print('white', white)

def clean_data(dir, file_name):
    if file_name[-5] != 'k':
        return 0
    global res
    image = cv2.imread(dir + file_name, cv2.IMREAD_GRAYSCALE)
    gray = len(image[np.logical_and(50 < image, image < 150)])
    black = len(image[image <= 50])
    white = len(image[image >= 150])
    if black > 0:
        if white < 0.05 * gray or white > 1.3 * gray:
            return 1
    else:
        if white < 0.01 * gray or white > 1.5 * gray:
            return 1
    return 0

dir1 = 'C:/Users/misha/Desktop/diploma/masked_AK_BKL_DF_SCC_VASC/'
dir2 = 'C:/Users/misha/Desktop/AK_BKL_DF_SCC_VASC_BAD_MASK/'

with os.scandir(dir1) as files:
    for file in files:
        if clean_data(dir1, file.name):
            shutil.move(dir1 + file.name, dir2 + file.name)
            shutil.move(dir1 + file.name[:-9] + '.jpg', dir2 + file.name[:-9] + '.jpg')





