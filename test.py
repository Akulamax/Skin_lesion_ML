import re
import pandas as pd
import os
import shutil
# a = ""
# print(len(a.split(',')))

# data1 = pd.read_csv(r'C:\Users\misha\Desktop\diploma\MEL_NV_BCC_0_4070_400.csv')
# data2 = pd.read_csv(r'C:\Users\misha\Desktop\diploma\MEL_NV_BCC_0_4070_total.csv')
# data = pd.concat([data1, data2])
# data = data.reset_index(drop=True)
# data.to_csv(r'C:\Users\misha\Desktop\diploma\MEL_NV_BCC_0_4070_all_total.csv')
#
# dir2 = 'C:/Users/misha/Desktop/diploma/masked_MEL_NV_BCC/'
# dir1 = 'C:/Users/misha/Desktop/Катя/'
# with os.scandir(dir1) as files:
#     for file in files:
#         if (int(file.name[5:12]) > 59000  and int(file.name[5:12]) < 61001) or (int(file.name[5:12]) > 64001  and int(file.name[5:12]) < 71199):
#             shutil.move(dir1 + file.name, dir2 + file.name)
# # shutil.move(dir2 + temp_filename, dir1 + temp_filename)
# print('lol')
# # a ='ISIC_0024478_mask.jpg'
# print(a[:-9] + '.jpg')
