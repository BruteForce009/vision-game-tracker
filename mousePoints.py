import cv2
import numpy as np

circles = np.zeros((4, 2), np.float32)
counter = 0


def mousePoints(event, x, y, flags, params):
    global counter
    if event == cv2.EVENT_LBUTTONDOWN:
        circles[counter] = x, y
        counter += 1


def getCalibrationMatrix(img, width = 640, height = 480):
    while True:
        if counter == 4:
            pts2 = np.float32([[0, 0], [width, 0], [0, height], [width, height]])
            matrix = cv2.getPerspectiveTransform(circles, pts2)
            # imgOutput = cv2.warpPerspective(img, matrix, (width, height))
            # cv2.imshow('Warp', imgOutput)
            break

        for x in range(4):
            cv2.circle(img, (int(circles[x][0]), int(circles[x][1])), 3, (0, 255, 0), cv2.FILLED)

        cv2.imshow('calibration', img)
        cv2.setMouseCallback('calibration', mousePoints)
        cv2.waitKey(1)

    cv2.destroyWindow('calibration')
    return matrix, circles


# cap = cv2.VideoCapture('balls.mp4')
# ret, img = cap.read()
# img = cv2.resize(img, (640, 480))
# width, height = 640, 480
#
# while True:
#     if counter == 4:
#         pts2 = np.float32([[0, 0], [width, 0], [0, height], [width, height]])
#         matrix = cv2.getPerspectiveTransform(circles, pts2)
#         imgOutput = cv2.warpPerspective(img, matrix, (width, height))
#         # cv2.imshow('Warp', imgOutput)
#         break
#
#     for x in range(4):
#         cv2.circle(img, (int(circles[x][0]), int(circles[x][1])), 3, (0, 255, 0), cv2.FILLED)
#
#     cv2.imshow('cards', img)
#     cv2.setMouseCallback('cards', mousePoints)
#     cv2.waitKey(1)
#
# cv2.destroyAllWindows()
#
# while True:
#     ret, img = cap.read()
#     if not ret:
#         # Play again
#         cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
#         continue
#     img = cv2.resize(img, (640, 480))
#     img = cv2.warpPerspective(img, matrix, (width, height))
#
#     cv2.imshow('Warp Feed', img)
#
#     if cv2.waitKey(10) & 0xFF == ord('q'):
#         break
#
# cap.release()
# cv2.destroyAllWindows()
