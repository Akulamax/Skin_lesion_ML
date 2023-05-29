import shutil
import os
import sys



good_image = ""
good_image = good_image.replace(' ', '')


good_image_list = good_image.split(',')


total_set = set(good_image_list)
print(len(total_set))

dir1 = 'C:/Users/misha/Desktop/diploma/masked_MEL_NV_BCC/'
dir2 = 'C:/Users/misha/Desktop/diploma/masked_MEL_NV_BCC_2/'

with os.scandir(dir1) as files:
    for file in files:
        number = file.name[5:12]
        while number[0] == '0':
            number = number[1:]
        number = int(number)
        if number > 71198:
            sys.exit(0)
        if str(number) in total_set:
            shutil.move(dir1 + file.name, dir2 + file.name)
