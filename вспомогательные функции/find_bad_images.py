import cv2
import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt
import shutil
import os
import sys
import re

# dir = 'C:/Users/misha/Desktop/diploma/masked_MEL_NV_BCC/'
# with os.scandir(dir) as files:
#     start_time = datetime.now()
#     print(start_time)
#     for index, file in enumerate(files, start=1):
#         if 1300 < int(file.name[8:12]) < 9860 and file.name[-5] != 'k':
#             res.append(file.name[8:12])
#         if int(file.name[8:12]) > 9860:
#            break
# print(datetime.now() - start_time)

bad_mask = ""
bad_image = ""
not_good_not_bad = ""


bad_image = bad_image.replace(' ', '')
bad_mask = bad_mask.replace(' ', '')
not_good_not_bad = not_good_not_bad.replace(' ', '')

bad_image_list = bad_image.split(',')
bad_mask_list = bad_mask.split(',')
not_good_not_bad_list = not_good_not_bad.split(',')

print(len(bad_image_list), len(bad_mask_list), len(not_good_not_bad_list), )
total_set = set(bad_image_list + bad_mask_list + not_good_not_bad_list)
print(len(total_set))
print(len(set(not_good_not_bad_list + bad_mask_list)))
dir1 = 'C:/Users/misha/Desktop/diploma/masked_MEL_NV_BCC/'
dir2 = 'C:/Users/misha/Desktop/diploma/clean_masked_MEL_NV_BCC_4/'

with os.scandir(dir1) as files:
    for file in files:
        number = file.name[5:12]
        while number[0] == '0':
            number = number[1:]
        number = int(number)
        if number < 29722:
            continue
        if file.name == 'ISIC_0065517':
            break
        if number > 65516:
            sys.exit(0)
        if str(number) in total_set:
            continue
        elif file.name[-5] == 'k':
            shutil.move(dir1 + file.name, dir2 + file.name)
