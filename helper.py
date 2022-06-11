import cv2
import numpy as np

def stackImages(scale, imgArray):
    rows = len(imgArray)
    cols = len(imgArray[0])
    rowsAvailable = isinstance(imgArray[0], list)
    width = imgArray[0][0].shape[1]
    height = imgArray[0][0].shape[0]

    if rowsAvailable:
        for x in range(rows):
            for y in range(cols):
                if imgArray[x][y].shape[:2] == imgArray[0][0].shape[:2]:
                    imgArray[x][y] = cv2.resize(imgArray[x][y], (0, 0), None, scale, scale)
                else:
                    imgArray[x][y] = cv2.resize(imgArray[x][y], (imgArray[0][0].shape[1],
                                                                 imgArray[0][0].shape[0]), None, scale, scale)
                if len(img[x][y].shape) == 2:
                    imgArray[x][y] = cv2.cvtColor(imgArray[x][y], cv2.COLOR_GRAY2BGR)

        imageBlank = np.zeros((height, width, 3), np.uint8)
        hor = [imageBlank] * rows
        hor_con = [imageBlank] * rows

        for x in range(rows):
            hor[x] = np.hstack(imgArray[x])
        ver = np.vstack(hor)
    else:
        for x in range(rows):
            if imgArray[x].shape[:2] == imgArray[0].shape[:2]:
                imgArray[x] = cv2.resize(imgArray[x], (0, 0), None, scale, scale)
            else:
                imgArray[x] = cv2.resize(imgArray[x], (imgArray[0].shape[1],
                                                       imgArray[0].shape[0]), None, scale, scale)
            if len(imgArray[x].shape) == 2:
                imgArray[x] = cv2.cvtColor(imgArray[x], cv2.COLOR_GRAY2BGR)
        hor = np.hstack(imgArray)
        ver = hor

    return ver

def empty(a):
    pass


def crop(img, circles, width = 640, height = 480):
    x1, y1 = circles[0].astype(int)
    x2, y2 = circles[-1].astype(int)
    img = img[y1 : y2, x1 : x2]
    img = cv2.resize(img, (width, height))
    return img


def IoU(cnt1, cnt2):
    x1, y1, w1, h1 = cv2.boundingRect(cnt1)
    x3, y3, w3, h3 = cv2.boundingRect(cnt2)
    x2 = x1 + w1
    y2 = y1 + h1
    x4 = x3 + w3
    y4 = y3 + h3

    x_inter1 = max(x1, x3)
    y_inter1 = max(y1, y3)
    x_inter2 = min(x2, x4)
    y_inter2 = min(y2, y4)

    width_inter = abs(x_inter2 - x_inter1)
    height_inter = abs(y_inter2 - y_inter1)
    area_inter = width_inter * height_inter

    area_box1 = w1 * h1
    area_box2 = w3 * h3
    area_union = area_box1 + area_box2 - area_inter
    iou = area_inter/area_union
    return  iou





