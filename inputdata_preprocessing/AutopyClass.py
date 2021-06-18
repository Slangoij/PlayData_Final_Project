import sys
import pyautogui
import time
import datetime
import cv2

# def enterCommand(command):
#     if len(command)>1:
#         for i in command:
#             pyautogui.keyDown(i)
#             time.sleep(0.1)
#         for t in reversed(command):
#             pyautogui.keyUp(t)
#             time.sleep(0.1)

#     else:
#         pyautogui.press(command)

def window_controller(pred):
    if pred == 0: # backward
        pyautogui.keyDown('ctrl')
        time.sleep(0.1)
        pyautogui.keyUp('')
    elif pred == 1: # fast_forward
        pyautogui.hotkey('right')
    elif pred == 2: # forward
        pyautogui.hotkey('ctrl', 'right')
    else:
        pass

cap = cv2.videoCapture(0)

# while True:
#     _, img = cap.read()
#     if not _ :
#         sys.exit()
    
#     cv2.imshow('img', img)

#     if cv2.waitKey(1) == ord
