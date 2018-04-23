#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import cv2
import numpy as np
import math
import xmlrpc.client
import time

s = xmlrpc.client.ServerProxy('http://192.168.8.172:8000')

gain = 128

# создаем объект cap для захвата кадров с камеры
cap = cv2.VideoCapture(0) # /dev/video0
hsvMin = np.array((54, 129, 0), np.uint8)
hsvMax = np.array((255, 255, 255), np.uint8)

while True:
    ret, frame = cap.read() #захватываем кадр
    if ret:
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)#преобразуем в HSV
        blur = cv2.GaussianBlur(hsv, (5, 5), 2)# размываем изображение blur
        thresh = cv2.inRange(hsv, hsvMin, hsvMax,)
        
        _, contours, hierarchy  = cv2.findContours(thresh.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)#находим контуры
        '''   
        if contours:
            # берем максимальный контур по периметру
            mainContour = max(contours, key = cv2.contourArea)
            M = cv2.moments(thresh)  #находим моменты
            if len(mainContour) > 4:
                ellipse = cv2.fitEllipse(mainContour)
                cv2.ellipse(frame, ellipse, (0,255,0), 2)
                '''
        for contour in contours:
            rect = cv2.minAreaRect(contour)#квадратный контур
            area = int(rect[1][0]*rect[1][1])
            if area > 10000:
                center = ((int(rect[0][0])), ((int(rect[0][1]))))#центр квадрата
                box = cv2.boxPoints(rect)#вершины квадрата
                box = np.int0(box)#округление координат

                edge1 = np.int0((box[1][0] - box[0][0], box[1][1] - box[1][0]))
                edge2 = np.int0((box[2][0] - box[1][0], box[2][1] - box[1][1]))

                usedEdge = edge1
                if cv2.norm(edge2) > cv2.norm(edge1):
                    usedEdge = edge2
                
                horizont = (1,0)
                angle = 180.0/math.pi * math.acos((horizont[0] * usedEdge[0] + horizont[1] * usedEdge[1]) / (cv2.norm(horizont) * cv2.norm(usedEdge)))
                
                cv2.drawContours(frame, [box], 0, (255,0,0), 2)#рисуем прямоугольник
                cv2.circle(frame, center,5, (0,0,255), 2)
                cv2.putText(frame, '%d' % int(angle), (center[0]+20, center[1]-20), cv2.FONT_HERSHEY_COMPLEX, 1, (0,0,255), 2)
            
        cv2.imshow('Frame', frame) #отображаем кадр

        res, imgJpg = cv2.imencode('.jpg', frame)
        if res:
            s.debugFrame(('Sandrolek', imgJpg.tobytes())) # заслал картинку
        
        key = cv2.waitKey(1) & 0xFF  #ждем нажатия клавиши
        if key == ord('q'): #если нажата Q тогда выходим
            break
    else:
        break

cap.release() #освобождаем cap
cv2.destroyAllWindows() #закрываем все окна

