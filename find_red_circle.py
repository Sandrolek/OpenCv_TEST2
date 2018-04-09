#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import cv2
import numpy as np

gain = 128

# создаем объект cap для зачватов кадров с камеры
cap = cv2.VideoCapture(0)#/dev/video0
# задаем макс и мин значения
hsvMin = np.array((0, 166, 179), np.uint8)
hsvMax = np.array((255, 255, 255), np.uint8)

while True:
    ret, frame = cap.read() #заххватываем кадр

    if ret:
        # переводим из BGR в HSV 
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # применяем нужные значения
        thresh = cv2.inRange(hsv, hsvMin, hsvMax)
        
        cv2.imshow('hsv', thresh)#отображаем кадр

        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'): # ждем нажатия клавиш, если нажата Q, то выходим
            break
        
    else:
        break
        
cap.release()
cv2.destroyAllWindows() #закрываем все окна
