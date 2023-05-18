import numpy as np
from matplotlib import pyplot as plt
import cv2

def cut_image(image_path):
    img = cv2.imread(image_path, 1)
    crop_img1 = img[97:623, 90:876]
    crop_img2 = img[270:486, 315:671]
    crop_img3 = img[3:126, 1:135]
    crop_img4 = img[161:329, 184:386]
    return [img, crop_img1, crop_img2, crop_img3, crop_img4]

def collect_colors(image_path): #'/kaggle/input/isic-2019-skin-lesion-images-for-classification/NV/ISIC_0000000.jpg'
    img = cv2.imread(image_path, 1)
    rgb_image = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = rgb_image
    gray_image = cv2.cvtColor(rgb_image, cv2.COLOR_RGB2GRAY)
    laplacian=cv2.Laplacian(img,cv2.CV_64F)
    sobelx=cv2.Sobel(img,cv2.CV_64F,1,0,ksize=5)
    sobely=cv2.Sobel(img,cv2.CV_64F,0,1,ksize=5)
    sobelx2=cv2.Sobel(img,cv2.CV_64F,2,0,ksize=5)
    sobely2=cv2.Sobel(img,cv2.CV_64F,0,2,ksize=5)
    sobelx8u = cv2.Sobel(img,cv2.CV_8U,1,0,ksize=5)
    sobelx64f = cv2.Sobel(img,cv2.CV_64F,1,0,ksize=5)
    abs_sobel64f = np.absolute(sobelx64f)
    sobel_8u = np.uint8(abs_sobel64f)
    result = []
    result.append(rgb_image.ravel())
    result.append(rgb_image[:,:,0].ravel())
    result.append(rgb_image[:,:,1].ravel())
    result.append(rgb_image[:,:,2].ravel())
    result.append(gray_image.ravel())
    result.append(laplacian.ravel())
    result.append(laplacian[:,:,0].ravel())
    result.append(laplacian[:,:,1].ravel())
    result.append(laplacian[:,:,2].ravel())
    result.append(sobelx.ravel())
    result.append(sobelx[:,:,0].ravel())
    result.append(sobelx[:,:,1].ravel())
    result.append(sobelx[:,:,2].ravel())
    result.append(sobely.ravel())
    result.append(sobely[:,:,0].ravel())
    result.append(sobely[:,:,1].ravel())
    result.append(sobely[:,:,2].ravel())
    result.append(sobelx2.ravel())
    result.append(sobelx2[:,:,0].ravel())
    result.append(sobelx2[:,:,1].ravel())
    result.append(sobelx2[:,:,2].ravel())
    result.append(sobely2.ravel())
    result.append(sobely2[:,:,0].ravel())
    result.append(sobely2[:,:,1].ravel())
    result.append(sobely2[:,:,2].ravel())
    result.append(sobelx8u.ravel())
    result.append(sobelx8u[:,:,0].ravel())
    result.append(sobelx8u[:,:,1].ravel())
    result.append(sobelx8u[:,:,2].ravel())
    result.append(sobel_8u.ravel())
    result.append(sobel_8u[:,:,0].ravel())
    result.append(sobel_8u[:,:,1].ravel())
    result.append(sobel_8u[:,:,2].ravel())
    return result
#img = cv2.imread(r'C:\Users\misha\Desktop\ISIC_0000000.jpg', 1)

def get_params(img):
    res = np.quantile(img,[0.05, 0.10, 0.15, 0.20, 0.25, 0.30, 0.35, 0.40, 0.45, 0.50, 0.55, 0.60, 0.65, 0.70, 0.75, 0.80, 0.85, 0.90, 0.95])
    res = np.append(res, np.min(img))
    res = np.append(res, np.mean(img))
    res = np.append(res, np.max(img))
    res = np.append(res, np.std(img))
    return res

x = map(get_params, collect_colors(r'C:\Users\misha\Desktop\ISIC_0000000.jpg'))
