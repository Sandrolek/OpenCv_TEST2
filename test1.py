#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import cv2

gain = 128

# создаем объект cap для зачватов кадров с камеры
cap = cv2.VideoCapture(0)#/dev/video0

while True:
    ret, frame = cap.read() #заххватываем кадр

    if ret:
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) # преобразуем в черно-белое

        # размываем изображение
        blur = cv2.GaussianBlur(gray, (5, 5), 0)
        
        # бинаризация в чб (исходное изобр, порогб макс. знач, 
        _, thresh = cv2.threshold(blur, gain, 255, cv2.THRESH_BINARY_INV)

        #ищем контуры на полученном изображении
        _, contours, _ = cv2.findContours(thresh.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        
        if contours:
            
            #находим самый большой контур
            mainContour = max(contours, key = cv2.contourArea)
            M = cv2.moments(mainContour) # находим моменты
            if M['m00'] != 0:#если нет деления на ноль
                cx = int(M['m10']/M['m00'])#смотрим координаты центра самого большого пятна
                cy = int(M['m01']/M['m00'])#они получаются в пикселях

                #рисуем перекрестье на контуре
                cv2.line(frame, (cx, 0), (cx, 1280), (255, 0, 0), 1)
                cv2.line(frame, (0, cy), (720, cy), (255, 0, 0), 1)
            
            #добавляем контуры на изображение
            cv2.drawContours(frame, mainContour, -1, (0, 255, 0), 2, cv2.FILLED)
            
        cv2.imshow('img1', frame)#отображаем кадр

        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'): # ждем нажатия клавиш, если нажата Q, то выходим
            break
        elif key == 45: #если нажали плюс
            gain -= 1
            print('Gain = %d' % gain)
        elif key == 43: #если нажали минус
            gain += 1
            print('Gain = %d' % gain)
    else:
        break
        
cap.release()
cv2.destroyAllWindows() #закрываем все окна
