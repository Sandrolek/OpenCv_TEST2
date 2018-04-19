#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import cv2 #Импорт сv2
import numpy as np

'''
Эта программа находит красный круг(с помощью нужного фильтра HSV) и рисует по его периметру эллипс
Значения фильтра HSV у каждого разные
Используются моменты из OpenCv 
'''

#Создаем объект кап для захвата видео с камеры
cap = cv2.VideoCapture(0) # /dev/video0

gain = 128

hsvMin = np.array((165, 66, 149), np.uint8)
hsvMax = np.array((255,255,255), np.uint8)

while True:
    
    ret, frame = cap.read() #Захватываем кадр
    
    if ret: #Проверка на успешность
        
        frame = cv2.GaussianBlur(frame, (5,5), 5) # размываем изображение
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV) # переводим его в HSV
        thresh = cv2.inRange(hsv,hsvMin,hsvMax) # устанавливаем фильтр изображения

        _, contours, _= cv2.findContours(thresh.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE) # находим все контуры
        
        if contours:
            mainContour = max(contours, key = cv2.contourArea) #Берем максимальный контур по периметру

            M = cv2.moments(mainContour) # берем все моменты

            if len(mainContour) > 4:
                # рисуем по перимитру наибольшего контура эллипс
                ellipse = cv2.fitEllipse(mainContour)
                cv2.ellipse(frame, ellipse, (42, 65, 74),5)
                
            dArea = M['m00']
            sumX = M['m10']
            sumY = M['m01']
            
            if M['m00'] != 0:
                cx = int(sumX/dArea) #Вычисляем координаты центра контура
                cy = int(sumY/dArea)

        cv2.imshow('hsv', frame) #Отображаем кадр
        cv2.imshow('prog', thresh) #Отображаем кадр
        
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'): #Проверка на нажатие клавиши
            break #Выход из цикла      
            
    else:
        break
cap.release() #Освобождаем кап
cv2.destroyAllWindows() #Закрываем окно
