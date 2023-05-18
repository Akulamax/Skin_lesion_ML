# importing the module
import cv2
from PIL import Image
import numpy as np
import plotly.express as px

res = []
# function to display the coordinates of
# of the points clicked on the image
def click_event(event, x, y, flags, params):
    #checking for left mouse clicks
    if event == cv2.EVENT_LBUTTONDOWN:
        # displaying the coordinates
        # on the Shell
        res.append([x, y])
        cv2.line(img, (x, y), (x, y), (255, 0, 255), thickness=3, lineType=cv2.LINE_8)
        cv2.imshow('image', img)
        if len(res) % 2 == 0:
            tmp = len(res) - 2
            cv2.rectangle(img, (res[tmp][0], res[tmp][1]), (res[tmp + 1][0], res[tmp + 1][1]), (255, 0, 255), thickness=1, lineType=cv2.LINE_8)
            cv2.imshow('image', img)


# driver function
if __name__ == "__main__":
    # reading the image
    img = cv2.imread(r'C:\Users\misha\Desktop\diploma\ISIC_0000000.jpg', 1)
    # displaying the image
    cv2.imshow('image', img)

    # setting mouse handler for the image
    # and calling the click_event() function
    cv2.setMouseCallback('image', click_event)

    cv2.waitKey(0)

    print(res)





    # wait for a key to be pressed to exit


    # close the window
    cv2.destroyAllWindows()