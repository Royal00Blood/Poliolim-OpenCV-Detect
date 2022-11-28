import cv2 as cv

img = cv.imread('0202.jpg')

def on_EVENT_LBUTTONDOWN(event, x, y, flags, param):
    if event == cv.EVENT_LBUTTONDOWN:
        xy = "%d,%d" % (x, y)
        cv.circle(img, (x, y), 1, (255, 0, 0), thickness=-1)
        cv.putText(img, xy, (x, y), cv.FONT_HERSHEY_PLAIN,
                    1.0, (0, 0, 0), thickness=1)
        cv.imshow("image", img)


cv.namedWindow("image")
cv.setMouseCallback("image", on_EVENT_LBUTTONDOWN)
while 1:
    cv.imshow("image", img)
    if cv.waitKey(0) & 0xFF == 27:
        break
cv.destroyAllWindows()
