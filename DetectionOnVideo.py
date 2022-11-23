import numpy as np
import cv2 as cv
import ColorTrecbar as ct
# import argparse
# parser = argparse.ArgumentParser(description='This sample demonstrates the meanshift algorithm. \
#                                               The example file can be downloaded from: \
#                                               https://www.bogotobogo.com/python/OpenCV_Python/images/mean_shift_tracking/slow_traffic_small.mp4')
# parser.add_argument('image', type=str, help='path to image file')
# args = parser.parse_args()
cap = cv.VideoCapture(0)  # (args.image)
############################ Video color ###############################################################################
# while True:
#     ret, frame = cap.read()
#     if frame is None:
#         break
#     frame_HSV = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
#     frame_threshold = cv.inRange(frame_HSV, (ct.low_H, ct.low_S, ct.low_V), (ct.high_H, ct.high_S, ct.high_V))
#     cv.imshow(ct.window_capture_name, frame)
#     cv.imshow(ct.window_detection_name, frame_threshold)
#     low_H, low_S, low_V, high_H, high_S, high_V = ct.low_H, ct.low_S, ct.low_V, ct.high_H, ct.high_S, ct.high_V
#     key = cv.waitKey(30)
#     if key == ord('q') or key == 27:
#         break
########################################################################################################################
# print( low_H, low_S, low_V, high_H, high_S, high_V)
# take first frame of the video
ret, frame = cap.read()
# setup initial location of window
x, y, w, h = 1105, 525, 150, 150
track_window = (x, y, w, h)
# set up the ROI for tracking
roi = frame[y:y+h, x:x+w]
hsv_roi = cv.cvtColor(roi, cv.COLOR_BGR2HSV)

mask = cv.inRange(hsv_roi, np.array((133., 0., 227.)), np.array((180., 255., 255.)))
roi_hist = cv.calcHist([hsv_roi], [0], mask, [180], [0, 180])
cv.normalize(roi_hist, roi_hist, 0, 255, cv.NORM_MINMAX)
# Setup the termination criteria, either 10 iteration or move by at least 1 pt
term_crit = (cv.TERM_CRITERIA_EPS | cv.TERM_CRITERIA_COUNT, 10, 1)
while 1:
    ret, frame = cap.read()
    if ret:
        hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
        dst = cv.calcBackProject([hsv], [0], roi_hist, [0, 180], 1)
        # apply meanshift to get the new location
        ret, track_window = cv.meanShift(dst, track_window, term_crit)
        # Draw it on image
        x, y, w, h = track_window
        img2 = cv.rectangle(frame, (x, y), (x+w, y+h), 255, 2)
        cv.imshow('img2', img2)
        k = cv.waitKey(30) & 0xff
        if k == 27:
            break
    else:
        break
