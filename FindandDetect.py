# Libraries
########################################################################################################################
import numpy as np
import cv2 as cv
import matplotlib.pyplot as plt
########################################################################################################################
# Custom Functions
########################################################################################################################
# _Функция получение координат точки или обьекта по щелчку мыши (Function to get the coordinates of a point or
# object on a mouse click)
def TakeCoordinates(event, x_cord, y_cord, flags, param):
    pixelCord[0] = x_cord
    pixelCord[1] = y_cord
    x_cord, y_cord = ConvertationPixelINCoordinates(x_cord, y_cord)
    if event == cv.EVENT_LBUTTONDOWN:
        xy_coordinates[0] = x_cord
        xy_coordinates[1] = y_cord
        if len(data_inf) <= (injured_number * 2):
            data_inf.append(xy_coordinates[0])
            data_inf.append(xy_coordinates[1])
        else:
            if len(data_img) < 4:
                data_img.append(xy_coordinates[0])
                data_img.append(xy_coordinates[1])

# _Функция определения ориентации //Написать//(Object Orientation Function)
def Object_Orientation_Function():
    angle = 1
    return angle

# _Расчет центра квадрата, описывающего искомый обьект
# (Calculation of the center of the square describing the desired object)
def CalculationCenterSquare(number_1, number_2):
    x_cord = number_1 / 5
    y_cord = number_2 / 5
    return x_cord, y_cord

# Преобразование пикселей в координаты
def ConvertationPixelINCoordinates(x_conv, y_conv):
    q = 1.57
    cord_x = x_conv * q
    cord_y = y_conv * q
    return cord_x, cord_y
# Выделение области захвата. (Selection of the capture area)
def AreaInit(img_in, list_data):
    if len(list_data) >= 4:
        # Координаты двух точек прямоугольника искомого изображения
        x_1 = list_data[0]
        y_1 = list_data[1]
        x_2 = list_data[2]
        y_2 = list_data[3]
        # Получение изображения
        if x_1 > x_2:
            if y_1 > y_2:
                img_cut = img_in[x_2:x_1, y_2:y_1]
            else:
                img_cut = img_in[x_2:x_1, y_1:y_2]
        else:
            if y_1 > y_2:
                img_cut = img_in[x_1:x_2, y_2:y_1]
            else:
                img_cut = img_in[x_1:x_2, y_1:y_2]
        plt.imsave("img_cut.jpg", img_cut)
########################################################################################################################
# __Переменные__(Variables)
# __Количество целевых точек__(Number of target points)
injured_number = int(input("Input number of injured "))
# __Списки данных__(Data Lists)
xy_coordinates = [0, 0]
data_cord = [0, 0]
data_inf = []
data_img = []
pixelCord = [0, 0]
# __
k_take_xy, x_sum, y_sum, w_sum, h_sum = 0, 0, 0, 0, 0
########################################################################################################################
# __Оновная программа__(Main)
# __ Часть первая. Чтение видео-потока.
cap = cv.VideoCapture(0)#("C:/Users/User_I/Desktop/Poliolimp/bandicam.mp4")
template = cv.imread('C:/Users/User_I/Desktop/Poliolimp/img2.png', 0)
w, h = template.shape[::-1]
methods = ['cv.TM_CCOEFF', 'cv.TM_CCOEFF_NORMED', 'cv.TM_CCORR',
           'cv.TM_CCORR_NORMED', 'cv.TM_SQDIFF', 'cv.TM_SQDIFF_NORMED']
if not cap.isOpened():
    print("Error video opened") # Ошибка открытия видео
    exit()
##########################################################################################
while True:
    # Захват кадр за кадром (Capture frame by frame)
    ret, frame = cap.read()
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...") # Не удается получить кадр (конец потока?). Выход...
        break
    ##########################################################################################
    AreaInit(frame, data_img)
    ##########################################################################################
    # for meth in methods:
    #     _, img = cap.read()
    #     method = eval(meth)
    #     # Apply template Matching
    #     img = cv.cvtColor(img, cv.COLOR_RGB2GRAY)
    #     res = cv.matchTemplate(img, template, method)
    #     min_val, max_val, min_loc, max_loc = cv.minMaxLoc(res)
    #     # If the method is TM_SQDIFF or TM_SQDIFF_NORMED, take minimum
    #     if method in [cv.TM_SQDIFF, cv.TM_SQDIFF_NORMED]:
    #         top_left = min_loc
    #     else:
    #         top_left = max_loc
    #     x, y = top_left[0], top_left[1]
    ######################################################################################
    cv.setMouseCallback("image", TakeCoordinates)

    x, y = pixelCord[0], pixelCord[1]
    w1, h1 = 60, 60  # 150, 150
    track_window = (x, y, w1, h1)
    # set up the ROI for tracking
    roi = frame[y:y + h, x:x + w]
    hsv_roi = cv.cvtColor(roi, cv.COLOR_BGR2HSV)
    # mask = cv.inRange(hsv_roi, np.array((133., 0., 227.)), np.array((180., 255., 255.)))
    # mask = cv.inRange(hsv_roi, np.array((120., 110., 215.)), np.array((180., 255., 255.)))
    # 115 97 96 255 255 255
    mask = cv.inRange(hsv_roi, np.array((144., 0., 205.)), np.array((180., 153., 255.)))
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
                x_sum += x + w / 2
                y_sum += y + h / 2
                k_take_xy += 1
            else:
                data_cord[0], data_cord[1] = CalculationCenterSquare(x_sum, y_sum)
                k_take_xy, x_sum, y_sum = 0, 0, 0
            ###########################################################################################
            img2 = cv.rectangle(frame, (x, y), (x + w, y + h), 255, 2)
            ###########################################################################################
            img = cv.cvtColor(frame, cv.COLOR_RGB2GRAY)
            cv.namedWindow("image")
            cv.setMouseCallback("image", TakeCoordinates)
            ###########################################################################################
            ###########################################################################################
            if (injured_number * 2) == len(data_inf):
                data_inf.append(x)
                data_inf.append(y)
                data_inf.append(Object_Orientation_Function())
            if (injured_number * 2) < len(data_inf):
                data_inf[injured_number * 2] = x
                data_inf[injured_number * 2 + 1] = y
                data_inf[injured_number * 2 + 2] = Object_Orientation_Function()
            ###########################################################################################
            print("data_cord = ", data_cord)
            print("xy_coordinates = ", xy_coordinates)
            print("data_inf = ", data_inf)
            ############################################################################################################
            cv.imshow('image', img2)
            k = cv.waitKey(30) & 0xff
            if k == 27:
                break
        else:
            break
# cv.putText(img2, "%d-%d" % (x, y), (x + 10, y - 10), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)