import cv2
import numpy as np
from helper import *
from mousePoints import *

# url = 'http://192.168.29.150:8080/video'
# cap = cv2.VideoCapture(url)

cv2.namedWindow('Parameters')
cv2.resizeWindow('Parameters', 640, 120)
cv2.createTrackbar('Threshold1', 'Parameters', 237, 255, empty)
cv2.createTrackbar('Threshold2', 'Parameters', 79, 255, empty)
cv2.createTrackbar('Min Area', 'Parameters', 1050, 10000, empty)


def getContours(img, imgContour):
    contours, hierarchy = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    # prev_contours = []
    i = 0
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > minArea:
            # flag = False
            # for cnt2 in prev_contours:
            #     if IoU(cnt, cnt2) > 0.9:
            #         flag = True
            #         break

            # if current box is not overlapping with previous boxes
            # if not flag:
            x, y, w, h = cv2.boundingRect(cnt)
            cv2.rectangle(imgContour, (x, y), (x + w, y + h), (0, 255, 0), 3)
            cv2.circle(imgContour, (int(x + w/2), int(y + h/2)), 5, (255, 255, 255), cv2.FILLED)
            cv2.putText(imgContour, '(' + str(int(x+w/2)) + ',' + str(int(y+h/2)) + ')', (int(x+w/4), int(y+h/1.4)),
                        cv2.FONT_HERSHEY_COMPLEX, 0.45, (255, 255, 255))
            i += 1
            # prev_contours.append(cnt)
            # print((x, y ,w, h))
    print(i)


cap = cv2.VideoCapture('side_balls.mp4')
width = 640
height = 480

ret, img = cap.read()
img = cv2.resize(img, (1000, 1000))
matrix, circles = getCalibrationMatrix(img, width, height)

while True:
    ret, img = cap.read()
    if not ret:
        # Play again
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
        continue

    img = cv2.resize(img, (1000, 1000))
    img = cv2.warpPerspective(img, matrix, (width, height))
    #img = crop(img, circles, width, height)

    imgContour = img.copy()
    #imgBlur = cv2.bilateralFilter(img, 9, 75, 75)
    imgBlur = cv2.GaussianBlur(img, (7, 7), 1)
    # imgBlur = cv2.blur(img, (3, 3))
    # imgBlur = cv2.medianBlur(img, 3)

    imgGray = cv2.cvtColor(imgBlur, cv2.COLOR_BGR2GRAY)

    threshold1 = cv2.getTrackbarPos('Threshold1', 'Parameters')
    threshold2 = cv2.getTrackbarPos('Threshold2', 'Parameters')
    minArea = cv2.getTrackbarPos('Min Area', 'Parameters')
    imgCanny = cv2.Canny(imgGray, threshold1, threshold2)
    kernel = np.ones((3, 4))
    imgDil = cv2.dilate(imgCanny, kernel, iterations=1)

    getContours(imgDil, imgContour)
    imgStack = stackImages(0.8, [imgBlur, imgDil, imgContour])

    cv2.imshow('Stack', imgStack)

    if cv2.waitKey(10) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
cap.release()
