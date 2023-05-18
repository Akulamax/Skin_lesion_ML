import sys

import cv2
import numpy as np
import random
from datetime import datetime
from scipy.stats import mode
import pandas as pd
import os
import sys

def get_markup(mask_name):
    dir1 = r'C:\Users\misha\Desktop\diploma\masked_MEL_NV_BCC\\'
    dir2 = r'C:\Users\misha\Desktop\diploma\clean_masked_MEL_NV_BCC_4\\'
    image = cv2.imread(dir1 + mask_name[:-9] + '.jpg', 1)
    mask = cv2.imread(dir2 + mask_name, 0)

    image[mask < 15] = [0, 0, 0]
    lesion = mask.copy()
    lesion[np.logical_and(0 < mask, mask < 170)] = 0
    skin = mask.copy()
    skin[mask > 0] = 0
    skin[np.logical_and(10 < mask, mask < 170)] = 255

    contours, hierarchy = cv2.findContours(image=lesion, mode=cv2.RETR_TREE, method=cv2.CHAIN_APPROX_NONE)

    sorted_cnt = sorted(contours, key=cv2.contourArea, reverse=True)
    if len(sorted_cnt) == 0:
        print('Не удалось выделить контур поражения', mask_name[:-9])
        return image, image, image, image, image
    cnt = sorted_cnt[0]
    if sorted_cnt[0][0][0][0] == 0 and sorted_cnt[0][0][0][1] == 0:
        cnt = sorted_cnt[1]
    tmp = len(cnt) - 1
    result_skin_and_lession = []
    diag = 100
    for i in range(9):
        if i == 8:
            break
        point = cnt[random.randint(int(tmp / 9 * i), int(tmp / 9 * (i + 1)))]
        point = (point[0][0], point[0][1])
        temp_rectangle = lesion[point[1] - diag:point[1] + diag,
                         point[0] - diag:point[0] + diag]  # y:y+height, x:x+width
        black_count = (temp_rectangle < 127).sum()
        all_count = (temp_rectangle >= 0).sum()
        if all_count != 0:
            result_skin_and_lession.append([black_count / all_count, point])

    if len(result_skin_and_lession) == 0:
        print('Не удалось выделить изображение кожи и поражения на изображении ', mask_name[:-9])
        skin_and_lession = image
    else:
        result_point = sorted(result_skin_and_lession, key=lambda value: np.abs(value[0] - 0.5))[0][1]
        skin_and_lession = image[result_point[1] - diag:result_point[1] + diag,
                           result_point[0] - diag:result_point[0] + diag]

    if len(cnt) != 0:
        x, y, w, h = cv2.boundingRect(cnt)
        all_lesion_and_skin = image[y:y + h, x:x + w]
    else:
        print('Не удалось выделить изображение кожи и всего поражения на изображении ', mask_name[:-9])
        all_lesion_and_skin = image

    lesion = cv2.bitwise_and(image, image, mask=lesion)
    skin = cv2.bitwise_and(image, image, mask=skin)

    return image, all_lesion_and_skin, lesion, skin, skin_and_lession


def collect_colors(image):
    img = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    xyz = cv2.cvtColor(image, cv2.COLOR_BGR2XYZ)
    yuv = cv2.cvtColor(image, cv2.COLOR_BGR2YUV)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    laplacian = cv2.Laplacian(img, cv2.CV_64F)
    sobelx = cv2.Sobel(img, cv2.CV_64F, 1, 0, ksize=5)
    sobely = cv2.Sobel(img, cv2.CV_64F, 0, 1, ksize=5)
    sobelx2 = cv2.Sobel(img, cv2.CV_64F, 2, 0, ksize=5)
    sobely2 = cv2.Sobel(img, cv2.CV_64F, 0, 2, ksize=5)
    sobelx8u = cv2.Sobel(img, cv2.CV_8U, 1, 0, ksize=5)
    sobelx64f = cv2.Sobel(img, cv2.CV_64F, 1, 0, ksize=5)
    abs_sobel64f = np.absolute(sobelx64f)
    sobel_8u = np.uint8(abs_sobel64f)
    result = []

    ravel = img.ravel()
    result.append(ravel[ravel > 0])
    ravel = img[:, :, 0].ravel()
    result.append(ravel[ravel > 0])
    ravel = img[:, :, 1].ravel()
    result.append(ravel[ravel > 0])
    ravel = img[:, :, 2].ravel()
    result.append(ravel[ravel > 0])

    ravel = hsv.ravel()
    result.append(ravel[ravel > 0])
    ravel = hsv[:, :, 0].ravel()
    result.append(ravel[ravel > 0])
    ravel = hsv[:, :, 1].ravel()
    result.append(ravel[ravel > 0])
    ravel = hsv[:, :, 2].ravel()
    result.append(ravel[ravel > 0])

    ravel = xyz.ravel()
    result.append(ravel[ravel > 0])
    ravel = xyz[:, :, 0].ravel()
    result.append(ravel[ravel > 0])
    ravel = xyz[:, :, 1].ravel()
    result.append(ravel[ravel > 0])
    ravel = xyz[:, :, 2].ravel()
    result.append(ravel[ravel > 0])

    ravel = yuv.ravel()
    result.append(ravel[ravel > 0])
    ravel = yuv[:, :, 0].ravel()
    result.append(ravel[ravel > 0])
    ravel = yuv[:, :, 1].ravel()
    result.append(ravel[ravel > 0])
    ravel = yuv[:, :, 2].ravel()
    result.append(ravel[ravel > 0])

    ravel = gray.ravel()
    result.append(ravel[ravel > 0])

    ravel = laplacian.ravel()
    result.append(ravel[ravel > 0])
    ravel = laplacian[:, :, 0].ravel()
    result.append(ravel[ravel > 0])
    ravel = laplacian[:, :, 1].ravel()
    result.append(ravel[ravel > 0])
    ravel = laplacian[:, :, 2].ravel()
    result.append(ravel[ravel > 0])

    ravel = sobelx.ravel()
    result.append(ravel[ravel > 0])
    ravel = sobelx[:, :, 0].ravel()
    result.append(ravel[ravel > 0])
    ravel = sobelx[:, :, 1].ravel()
    result.append(ravel[ravel > 0])
    ravel = sobelx[:, :, 2].ravel()
    result.append(ravel[ravel > 0])

    ravel = sobely.ravel()
    result.append(ravel[ravel > 0])
    ravel = sobely[:, :, 0].ravel()
    result.append(ravel[ravel > 0])
    ravel = sobely[:, :, 1].ravel()
    result.append(ravel[ravel > 0])
    ravel = sobely[:, :, 2].ravel()
    result.append(ravel[ravel > 0])

    ravel = sobelx2.ravel()
    result.append(ravel[ravel > 0])
    ravel = sobelx2[:, :, 0].ravel()
    result.append(ravel[ravel > 0])
    ravel = sobelx2[:, :, 1].ravel()
    result.append(ravel[ravel > 0])
    ravel = sobelx2[:, :, 2].ravel()
    result.append(ravel[ravel > 0])

    ravel = sobely2.ravel()
    result.append(ravel[ravel > 0])
    ravel = sobely2[:, :, 0].ravel()
    result.append(ravel[ravel > 0])
    ravel = sobely2[:, :, 1].ravel()
    result.append(ravel[ravel > 0])
    ravel = sobely2[:, :, 2].ravel()
    result.append(ravel[ravel > 0])

    ravel = sobelx8u.ravel()
    result.append(ravel[ravel > 0])
    ravel = sobelx8u[:, :, 0].ravel()
    result.append(ravel[ravel > 0])
    ravel = sobelx8u[:, :, 1].ravel()
    result.append(ravel[ravel > 0])
    ravel = sobelx8u[:, :, 2].ravel()
    result.append(ravel[ravel > 0])

    ravel = sobel_8u.ravel()
    result.append(ravel[ravel > 0])
    ravel = sobel_8u[:, :, 0].ravel()
    result.append(ravel[ravel > 0])
    ravel = sobel_8u[:, :, 1].ravel()
    result.append(ravel[ravel > 0])
    ravel = sobel_8u[:, :, 2].ravel()
    result.append(ravel[ravel > 0])
    return result


def get_params(img):
    res = np.quantile(img,
                      [0.05, 0.10, 0.15, 0.20, 0.25, 0.30, 0.35, 0.40, 0.45, 0.50, 0.55, 0.60, 0.65, 0.70, 0.75, 0.80,
                       0.85, 0.90, 0.95])
    res = np.append(res, np.min(img))
    res = np.append(res, np.mean(img))
    res = np.append(res, np.max(img))
    res = np.append(res, np.std(img))
    res = np.append(res, mode(img).mode[0])
    res = np.append(res, np.median(img))
    return res


def get_total_params(mask_name):
    markup_images = get_markup(mask_name)
    result_params = []
    for img in markup_images:
        result_params += list(map(get_params, collect_colors(img)))
    total = []
    for params in result_params:
        total = np.hstack([total, params])
    total = np.append(total, mask_name[:-9])
    return total


def get_dataframe():
    img_color = ['rbg_full', 'rgb_r', 'rgb_g', 'rgb_b', 'hsv_full', 'hsv_h', 'hsv_s', 'hsv_v', 'xyz_full', 'xyz_x', 'xyz_y', 'xyz_z']
    img_color += ['yuv_full', 'yuv_y', 'yuv_u', 'yuv_v', 'gray', 'laplacian_full', 'laplacian_r', 'laplacian_g', 'laplacian_b']
    img_color += ['sobelx_full', 'sobelx_r', 'sobelx_g', 'sobelx_b', 'sobely_full', 'sobely_r', 'sobely_g', 'sobely_b']
    img_color += ['sobelx2_full', 'sobelx2_r', 'sobelx2_g', 'sobelx2_b', 'sobely2_full', 'sobely2_r', 'sobely2_g', 'sobely2_b']
    img_color += ['sobelx8u_full', 'sobelx8u_r', 'sobelx8u_g', 'sobelx8u_b', 'sobel_8u_full', 'sobel_8u_r', 'sobel_8u_g', 'sobel_8u_b']
    columns = []
    for j in ['I_', 'ALAS_', 'L_', 'S_', 'LAS_']:
        for k in range(len(img_color)):
            columns += [j + img_color[k] + '_Q' + str(i * 5) for i in range(1, 20)]
            columns += [j + img_color[k] + '_min', j + img_color[k] + '_mean', j + img_color[k] + '_max',
                        j + img_color[k] + '_std', j + img_color[k] + '_mode', j + img_color[k] + '_median']
    columns += ['image_name']
    df = pd.DataFrame(columns=columns)
    return df


dir = r'C:\Users\misha\Desktop\diploma\clean_masked_MEL_NV_BCC_4\\'

df = get_dataframe()
with os.scandir(dir) as files:
    start_time = datetime.now()
    print(start_time)
    for index, file in enumerate(files):
        total = get_total_params(file.name)
        df.loc[len(df.index)] = total
        if index % 100 == 0 and index != 0:
            print(index, datetime.now() - start_time)
            df.to_csv(rf'C:\Users\misha\Desktop\diploma\MEL_NV_BCC_4_{index}.csv')
df.to_csv(r'C:\Users\misha\Desktop\diploma\MEL_NV_BCC_4_total.csv')
print(datetime.now() - start_time)


