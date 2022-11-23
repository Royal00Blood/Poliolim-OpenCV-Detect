# import cv2
#
# def video_reader():
#     cam = cv2.VideoCapture(0) #включаем камеру
#     detector = cv2.QRCodeDetector() #включаем  QRCode detector
#     while True:
#         _, img = cam.read()
#         data, bbox, _ = detector.detectAndDecode(img)
#         if data:
#             print("QR Code detected-->", data)
#         cv2.imshow("img", img)
#         if cv2.waitKey(1) == ord("Q"):
#             break
#     cam.release()
#     cv2.destroyAllWindows()
#
# video_reader()

import cv2
import numpy as np
import sys
import time

if len(sys.argv)>1:
    inputImage = cv2.imread(sys.argv[1])
else:
    inputImage = cv2.imread("C:/Users/User_I/Desktop/images.png")


# Display barcode and QR code location
def display(im, bbox):
    n = len(bbox)
    for j in range(n):
        cv2.line(im, tuple(bbox[j][0]), tuple(bbox[(j + 1) % n][0]), (255, 0, 0), 3)

    # Display results
    cv2.imshow("Results", im)


qrDecoder = cv2.QRCodeDetector()

# Detect and decode the qrcode
data, bbox, rectifiedImage = qrDecoder.detectAndDecode(inputImage)
if len(data) > 0:
    print("Decoded Data : {}".format(data))
    display(inputImage, bbox)
    rectifiedImage = np.uint8(rectifiedImage)
    cv2.imshow("Rectified QRCode", rectifiedImage)
else:
    print("QR Code not detected")
    cv2.imshow("Results", inputImage)

cv2.waitKey(0)
cv2.destroyAllWindows()