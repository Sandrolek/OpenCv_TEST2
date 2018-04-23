#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import cv2
import time
from xmlrpc.server import SimpleXMLRPCServer
import numpy as np

DEBUG_PORT = 8000
IP_SERVER = '192.168.8.172'

serverDebug = SimpleXMLRPCServer((IP_SERVER, DEBUG_PORT))
serverDebug.logRequests = False

def debugFrame(frame):
    frameName = frame[0]
    imgArray = np.frombuffer(frame[1].data, dtype=np.uint8)
    img = cv2.imdecode(imgArray, cv2.IMREAD_COLOR)
    cv2.imshow(frameName, img)
    
    cv2.waitKey(1)
    return 0

serverDebug.register_function(debug_frame)

try:
    serverDebug.server_forever()
except (KeyboardInterrupt, SystemExit):
    print('Ctrl+C pressed')
    serverDebug.server_close()
cv2.destroyAllWindows()
