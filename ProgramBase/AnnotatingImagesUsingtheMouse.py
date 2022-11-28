# Import packages
import cv2 as cv
# Lists to store the bounding box coordinates
top_left_corner = []
bottom_right_corner = []
# function which will be called on mouse input
def drawRectangle(action, x, y, flags, *userdata):
    # Referencing global variables
    global top_left_corner, bottom_right_corner
    # Mark the top left corner when left mouse button is pressed
    if action == cv.EVENT_LBUTTONDOWN:
        top_left_corner = [(x, y)]
        # When left mouse button is released, mark bottom right corner
    elif action == cv.EVENT_LBUTTONUP:
        bottom_right_corner = [(x, y)]
        # Draw the rectangle
        cv.rectangle(frame, top_left_corner[0], bottom_right_corner[0], (0, 255, 0), 2, 8)
        #SaveIMG()
        cv.imshow("Window", frame)
        x1,y1 = top_left_corner[0]
        print(x1,y1)
        print(top_left_corner[0], bottom_right_corner[0])
#def SaveIMG():
cv.namedWindow("Window")
cap = cv.VideoCapture(0)

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()

    # Our operations on the frame come here
    cv.setMouseCallback("Window", drawRectangle)

    # Display the resulting frame
    cv.imshow('Window', frame)
    if cv.waitKey(1) & 0xFF == ord('q'):
        break
# When everything done, release the capture
cap.release()
cv.destroyAllWindows()