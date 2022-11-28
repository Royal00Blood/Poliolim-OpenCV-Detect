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
        cv.rectangle(image, top_left_corner[0], bottom_right_corner[0], (0, 255, 0), 2, 8)
        cv.imshow("Window", image)
        print(top_left_corner[0], bottom_right_corner[0])
# Read Images
image = cv.imread("C:/Users/User_I/PycharmProjects/Poliolim-OpenCV-Detect/data/0202.jpg")

# Make a temporary image, will be useful to clear the drawing
temp = image.copy()
# Create a named window
cv.namedWindow("Window")
# highgui function called when mouse events occur
cv.setMouseCallback("Window", drawRectangle)
k = 0
# Close the window when key q is pressed
while k != 113:
    # Display the image
    cv.imshow("Window", image)
    k = cv.waitKey(0)
    # If c is pressed, clear the window, using the dummy image
    if (k == 99):
        image = temp.copy()
        cv.imshow("Window", image)
cv.destroyAllWindows()