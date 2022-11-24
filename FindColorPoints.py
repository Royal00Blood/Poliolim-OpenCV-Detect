import cv2
import numpy as np
import ColorTrecbar as ct

if __name__ == '__main__':
    def callback(*arg):
        print(arg)


def ColorOn(cap):
    while True:
        ret, frame = cap.read()
        if frame is None:
            break
        frame_HSV = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        frame_threshold = cv2.inRange(frame_HSV, (ct.low_H, ct.low_S, ct.low_V), (ct.high_H, ct.high_S, ct.high_V))

        cv2.imshow(ct.window_capture_name, frame)
        cv2.imshow(ct.window_detection_name, frame_threshold)

        key = cv2.waitKey(30)
        if key == ord('q') or key == 27:
            return ct.low_H, ct.low_S, ct.low_V, ct.high_H, ct.high_S, ct.high_V


cv2.namedWindow("result")

cap = cv2.VideoCapture(0)
low_H, low_S, low_V, high_H, high_S, high_V = ColorOn(cap)
hsv_min = np.array((low_H, low_S, low_V), np.uint8)
hsv_max = np.array((high_H, high_S, high_V), np.uint8)

color_yellow = (0, 255, 255)


while True:
    flag, img = cap.read()
    img = cv2.flip(img, 1)  # отражение кадра вдоль оси Y
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    thresh = cv2.inRange(hsv, hsv_min, hsv_max)

    moments = cv2.moments(thresh, 1)
    dM01 = moments['m01']
    dM10 = moments['m10']
    dArea = moments['m00']

    if dArea > 100:
        x = int(dM10 / dArea)
        y = int(dM01 / dArea)
        cv2.circle(img, (x, y), 5, color_yellow, 2)
        cv2.putText(img, "%d-%d" % (x, y), (x + 10, y - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, color_yellow, 2)

    cv2.imshow('result', img)

    ch = cv2.waitKey(5)
    if ch == 27:
        break

cap.release()
cv2.destroyAllWindows()