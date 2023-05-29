import shutil
import os

dir1 = 'C:/Users/misha/Desktop/diploma/MEL_NV_BCC/'
dir2 = 'C:/Users/misha/Desktop/diploma/masked_MEL_NV_BCC/'

with os.scandir(dir1) as files:
    temp_filename = 'kkkkkkk'
    for file in files:
        if file.name[-5:-4] != 'k' and temp_filename[-5:-4] != 'k':
            break
        shutil.move(dir1 + file.name, dir2 + file.name)
        temp_filename = file.name
shutil.move(dir2 + temp_filename, dir1 + temp_filename)

