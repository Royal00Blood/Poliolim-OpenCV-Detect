import numpy as np
import cv2 as cv
import matplotlib.pyplot as plt
# pip3 install opencv-python qrcode
##########################################################################################
def TakeCoordinates(event, x_cord, y_cord, flags, param):
    if event == cv.EVENT_LBUTTONDOWN:
        xy_coordinates[0] = x_cord
        xy_coordinates[1] = y_cord

def CollectInformationArray(img):
    if len(data_inf) < (injured_number * 2):
        data_inf.append(xy_coordinates[0])
        data_inf.append(xy_coordinates[1])
    else:
        if len(data_img) < 4:
            data_img.append(xy_coordinates[0])
            data_img.append(xy_coordinates[1])
        else:
            AreaInit(img, data_img)
def TakeAngle():
    angle = 1  # Функция определения ориентации Написать
    return angle
def CalculationCenterSquare(number_1, number_2):  # x,y,w,h
    x_cord = number_1/5
    y_cord = number_2/5
    return x_cord, y_cord
def ConvertationPixelINCoordinates(x, y):
    ##### НАПИСАТЬ МЕТОД ########
    cord_x = 1###
    cord_y = 1###
    return cord_x, cord_y
# def FormationCommonList(data1, data2, data3):
#     common_list = []
#     for i in data1:
#         common_list.append(i)
#     for i in data2:
#         common_list.append(i)
#     for i in data3:
#         common_list.append(i)
#     return common_list
def AreaInit(img, list_data):
    # Координаты двух точек прямоугольника искомого изображения
    x_1 = list_data[0]
    y_1 = list_data[1]
    x_2 = list_data[2]
    y_2 = list_data[3]
    # Получение изображения
    if x_1 > x_2:
        if y_1>y_2:
            img_cut = img[x_2:x_1, y_2:y_1]
        else:
            img_cut = img[x_2:x_1, y_1:y_2]
    else:
        if y_1>y_2:
            img_cut = img[x_1:x_2, y_2:y_1]
        else:
            img_cut = img[x_1:x_2, y_1:y_2]
    plt.imsave("img_cut.jpg", img_cut)
##########################################################################################
injured_number = int(input("Input number of injured "))
xy_coordinates =[0, 0]
data_cord = [0, 0]
data_inf = []
data_img = []
k_take_xy, x_sum, y_sum, w_sum, h_sum = 0, 0, 0, 0, 0
########################################################################################3
cap = cv.VideoCapture(0)#("C:/Users/User_I/Desktop/bandicam.mp4")
template = cv.imread('C:/Users/User_I/Desktop/img2.png', 0)
w, h = template.shape[::-1]
methods = ['cv.TM_CCOEFF', 'cv.TM_CCOEFF_NORMED', 'cv.TM_CCORR',
           'cv.TM_CCORR_NORMED', 'cv.TM_SQDIFF', 'cv.TM_SQDIFF_NORMED']
if not cap.isOpened():
    print("Error video opened")
    exit()
##########################################################################################
while True:
    # Capture frame by frame
    ret, frame = cap.read()
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break
    ##########################################################################################
    CollectInformationArray(frame)
    ##########################################################################################
    for meth in methods:
        _, img = cap.read()
        method = eval(meth)
        # Apply template Matching
        img = cv.cvtColor(img, cv.COLOR_RGB2GRAY)
        res = cv.matchTemplate(img, template, method)
        min_val, max_val, min_loc, max_loc = cv.minMaxLoc(res)
        # If the method is TM_SQDIFF or TM_SQDIFF_NORMED, take minimum
        if method in [cv.TM_SQDIFF, cv.TM_SQDIFF_NORMED]:
            top_left = min_loc
        else:
            top_left = max_loc
        x, y = top_left[0], top_left[1]
    ######################################################################################
    w1, h1 =60, 60 # 150, 150
    track_window = (x, y, w1, h1)
    # set up the ROI for tracking
    roi = frame[y:y + h, x:x + w]
    hsv_roi = cv.cvtColor(roi, cv.COLOR_BGR2HSV)
    #mask = cv.inRange(hsv_roi, np.array((133., 0., 227.)), np.array((180., 255., 255.)))
    #mask = cv.inRange(hsv_roi, np.array((120., 110., 215.)), np.array((180., 255., 255.)))
    #115 97 96 255 255 255
    mask = cv.inRange(hsv_roi, np.array((131., 103., 216.)), np.array((255., 255., 255.)))
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
            ##############################################################################################
            if k_take_xy < 5:
                x_sum += x +w/2
                y_sum += y +h/2
                k_take_xy += 1
            else:
                data_cord[0], data_cord[1] = CalculationCenterSquare(x_sum, y_sum)
                k_take_xy, x_sum, y_sum = 0, 0, 0
            print("data_cord = ", data_cord)
            ###########################################################################################
            img2 = cv.rectangle(frame, (x, y), (x + w, y + h), 255, 2)
            ###########################################################################################
            img = cv.cvtColor(frame, cv.COLOR_RGB2GRAY)
            #print(data_inf[(injured_number*2)-1])
            cv.namedWindow("image")
            cv.setMouseCallback("image", TakeCoordinates)
            ###########################################################################################
            ###########################################################################################
            if (injured_number*2)==len(data_inf):
                data_inf.append(x)
                data_inf.append(y)
            if(injured_number*2) < len(data_inf):
                data_inf[injured_number*2] = x
                data_inf[injured_number * 2 + 1] = y
                #data_inf[injured_number * 2 + 2] = TakeAngle()
            ###########################################################################################
            cv.imshow('image', img2)
            k = cv.waitKey(30) & 0xff
            if k == 27:
                break
        else:
            break
