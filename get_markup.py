import cv2
import numpy as np
import random
# path to input image is specified and
# image is loaded with imread command
image = cv2.imread(r'C:\Users\misha\Desktop\diploma\masked_MEL_NV_BCC\ISIC_0010440.jpg', 1)
mask = cv2.imread(r'C:\Users\misha\Desktop\diploma\clean_masked_MEL_NV_BCC_0_4070\ISIC_0010440_mask.jpg', 0)

cv2.imshow('image', image)
cv2.imshow('mask', mask)

image[mask < 15] = 0
lesion = mask.copy()
lesion[np.logical_and(0 < mask, mask < 170)] = 0
skin = mask.copy()
skin[mask > 0] = 0
skin[np.logical_and(10 < mask, mask < 170)] = 255

cv2.imshow('lesion', cv2.bitwise_and(image, image, mask=lesion))
cv2.imshow('skin', cv2.bitwise_and(image, image, mask=skin))

contours, hierarchy = cv2.findContours(image=lesion, mode=cv2.RETR_TREE, method=cv2.CHAIN_APPROX_NONE)


tmp = 0
tmp_index = 0
# cnt = []

# for index, i in enumerate(contours):
#     if cv2.contourArea(i) > 4000 and len(i) > tmp and i[0][0][0] != 0 and i[0][0][1] != 0:
#         tmp = len(i) - 1
#         tmp_index = index
#         cnt = i
sorted_cnt = sorted(contours, key=cv2.contourArea, reverse=True)
cnt = sorted_cnt[0]
if sorted_cnt[0][0][0][0] == 0 and sorted_cnt[0][0][0][1] == 0:
    cnt = sorted_cnt[1]
tmp = len(cnt) - 1
result_skin_and_lession = []
diag = 100
for i in range(9):
        if i == 8:
            break
        point = cnt[random.randint(int(tmp/9 * i), int(tmp/9 * (i + 1)))]
        point = (point[0][0], point[0][1])
        temp_rectangle = lesion[point[1] - diag:point[1] + diag, point[0] - diag:point[0] + diag]  # y:y+height, x:x+width
        temp_height, temp_width = temp_rectangle.shape
        black_count = (temp_rectangle < 127).sum()
        all_count = (temp_rectangle >= 0).sum()
        if all_count != 0:
            result_skin_and_lession.append([black_count / all_count, point])

t = 1
result_point = -1
result_point = sorted(result_skin_and_lession, key=lambda value: np.abs(value[0] - 0.5))[0][1]


for i in result_skin_and_lession:
    if np.abs(i[0] - 0.5) < t:
        t = np.abs(i[0] - 0.5)
        result_point = i[1]
print(result_point)
if result_point == -1:
    print('Не удалось выделить изображение кожи и поражения на изображении')
skin_and_lession = image[result_point[1] - diag:result_point[1] + diag, result_point[0] - diag:result_point[0] + diag]


x, y, w, h = cv2.boundingRect(cnt)

all_lesion_and_skin = image[y:y+h, x:x+w]

cv2.imshow('skin_and_lesion', skin_and_lession)
cv2.imshow('all_lesion_and_skin', all_lesion_and_skin)
if cv2.waitKey(0) & 0xff == 27:
    cv2.destroyAllWindows()