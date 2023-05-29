import cv2
import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt
import shutil
import os
import time

def get_mask(path):
    image = cv2.imread(path)
    path = path[:-4] + '_mask' + path[-4:]
    height, width, _ = image.shape
    if height > width:
        print(path, 'this photo is trash')
        return 0
    flag = 0
    point2 = 5
    if image[int(height / 2), int(width - width / 32)].sum() < 60 and image[
        int(height / 2), int(width / 32)].sum() < 60 and image[
        int(height / 32), int(width / 2)].sum() < 60 and image[
        int(height - height / 32), int(width / 2)].sum() < 60:
        flag = 1
    if flag != 1 and (
            image[point2, point2].sum() < 450 or image[height - 1 - point2, point2].sum() < 450 or image[
        point2, width - 1 - point2].sum() < 450 or image[
                height - 1 - point2, width - 1 - point2].sum() < 450):
        flag = 2

    ravel = image.ravel()
    n, bins, _ = plt.hist(ravel[ravel > 10], bins=np.linspace(0, 255, 256))  # n - counts
    bins = np.delete(bins, 0)
    filter_n = n[n > 1000]
    quantile = np.quantile(filter_n, 0.2)
    tmp_amplitude = bins[n > quantile]
    amplitude = tmp_amplitude[len(tmp_amplitude) - 1] - tmp_amplitude[0]
    regime = 1

    if flag == 0:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (7, 7), 0)

        if 180 < amplitude < 220:
            regime = 2
        elif amplitude <= 180:
            regime = 3

        if regime == 1:
            C = 45
        elif regime == 2:
            C = 35
        else:
            C = -20

        tmp_amplitude_2 = bins[n > np.quantile(filter_n, 0.8)]

        amplitude_2 = tmp_amplitude_2[len(tmp_amplitude_2) - 1] - tmp_amplitude_2[0]
        if amplitude_2 < 66 and amplitude <= 180:
            C += 40

        thresh1 = cv2.adaptiveThreshold(blurred, 127, cv2.ADAPTIVE_THRESH_MEAN_C,
                                        cv2.THRESH_BINARY, 1001, C)
        total_mask = thresh1
        total_mask[total_mask == 0] = 255
        cv2.rectangle(total_mask, (0, 0), (width - 1, height - 1), (127, 0, 0), 5)

        cv2.imwrite(path, total_mask)

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

        h = height / 2
        w = width / 2
        for i in range(height):
            for j in range(width):
                if (i - h) ** 2 + (j - w) ** 2 > radius:
                    image[i, j] = 0

        if 80 < amplitude < 230:
            regime = 2
        elif amplitude >= 230:
            regime = 3

        if regime == 1:
            C = -65
        elif regime == 2:
            C = -45
        else:
            C = -5

        if 200 > amplitude > 110:
            if pt1 < 60 and pt2 > width - 60:
                C += 30
            if pt1 > 130 and pt2 < width - 130:
                C -= 30
        if pt1 > 160 and pt2 < width - 160 and amplitude >= 200:
            C -= 65

        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (7, 7), 0)

        (T, threshInv2) = cv2.threshold(blurred, 10, 255, cv2.THRESH_BINARY)

        masked = cv2.bitwise_and(image, image, mask=threshInv2)

        image_copy = masked.copy()
        gray = cv2.cvtColor(image_copy, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (7, 7), 0)

        thresh1 = cv2.adaptiveThreshold(blurred, 127, cv2.ADAPTIVE_THRESH_MEAN_C,
                                        cv2.THRESH_BINARY, 1001, C)

        contours, hierarchy = cv2.findContours(image=threshInv2, mode=cv2.RETR_TREE,
                                               method=cv2.CHAIN_APPROX_NONE)

        cv2.drawContours(image=threshInv2, contours=contours, contourIdx=-1, color=(0, 0, 0), thickness=5,
                         lineType=cv2.LINE_AA)

        skin = image
        skin[thresh1 == 127] = 127

        lesion = skin

        lesion[threshInv2 == 0] = 0
        lesion = cv2.cvtColor(lesion, cv2.COLOR_BGR2GRAY)
        lesion[np.logical_and(lesion != 0, thresh1 != 127)] = 255

        cv2.imwrite(path, lesion)

    if flag == 1:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (7, 7), 0)

        (T, threshInv2) = cv2.threshold(blurred, 10, 255, cv2.THRESH_BINARY)

        masked = cv2.bitwise_and(image, image, mask=threshInv2)

        if amplitude > 200:
            regime = 2

        if regime == 1:
            C = 5
        else:
            C = -20

        image_copy = masked.copy()
        gray = cv2.cvtColor(image_copy, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (7, 7), 0)

        thresh1 = cv2.adaptiveThreshold(blurred, 127, cv2.ADAPTIVE_THRESH_MEAN_C,
                                        cv2.THRESH_BINARY, 441, C)

        skin = image
        skin[thresh1 == 127] = 127

        lesion = skin
        contours, hierarchy = cv2.findContours(image=threshInv2, mode=cv2.RETR_TREE,
                                               method=cv2.CHAIN_APPROX_NONE)

        cv2.drawContours(image=threshInv2, contours=contours, contourIdx=-1, color=(0, 0, 0), thickness=75,
                         lineType=cv2.LINE_AA)

        lesion[threshInv2 == 0] = 0
        lesion = cv2.cvtColor(lesion, cv2.COLOR_BGR2GRAY)
        lesion[np.logical_and(lesion != 0, thresh1 != 127)] = 255

        cv2.imwrite(path, lesion)
    return 0

def run_forever():
    try:
        # Create infinite loop to simulate whatever is running
        # in your program
        while True:
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

            dir = 'C:/Users/misha/Desktop/diploma/MEL_NV_BCC/'
            with os.scandir(dir) as files:
                start_time = datetime.now()
                print(start_time)
                for index, file in enumerate(files, start=1):
                    get_mask(dir + file.name)
                    if index % 100 == 0:
                        print(index)
                        print(datetime.now() - start_time)
                        os.system(   )

            print(datetime.now() - start_time)
            raise Exception("Error simulated!")
    except Exception:
        print("Something crashed your program. Let's restart it")
        time.sleep(10)
        run_forever() # Careful.. recursive behavior
        # Recommended to do this instead
        handle_exception()

def handle_exception():
    # code here
    pass

run_forever()
