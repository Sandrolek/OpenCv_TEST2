#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
Данная программа позволяет найти наибольший зеленый четырехугольник и обрисовать по его контуру прямоугольник и его центр
Также программа показывает, на сколько градусов отклонен нарисованный прямоугольник от горизонта. Это определяется по одной из длинных граней прямоугольника
'''

import cv2 #Импорт сv2
import numpy as np

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
        blur = cv2.GaussianBlur(hsv, (5, 5, 0))
        thresh = cv2.inRange(blur ,hsvMin, hsvMax) # устанавливаем фильтр изображения

        _, contours, _= cv2.findContours(thresh.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE) # находим все контуры
        
        if contours:
            rect = cv2.minAreaRect(contour) # получаем контур квадрата
            area = int(rect[1][0]*rect[1][1])
            if area > 500:
                center = (int(rect[0][0]), int(rect[0][1]))
                
                box = cv2.boxPoints(rect) # вершины квадрата
                box = np.int0(box) # округляем все вершины

                edge1 = np.int0((box[1][0] - box[0][0], box[1][1] - box[0][1]))
                edge2 = np.int0((box[2][0] - box[1][0], box[2][1] - box[1][1]))

                cv2.drawContours(frame, [box], 0, (255, 0, 0), 2) # показыаем ы
                cv2.circle(frame, center, 5, (255, 0, 0), 3)
            
        cv2.imshow('hsv', frame) #Отображаем кадр
        cv2.imshow('prog', thresh) #Отображаем кадр
        
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'): #Проверка на нажатие клавиши
            break #Выход из цикла      
            
    else:
        break
cap.release() #Освобождаем кап
cv2.destroyAllWindows() #Закрываем окно
