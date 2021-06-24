import sys
import pyautogui
import time
import datetime
import cv2

def window_controller(pred):
    if pred == 0: # backward
        # pyautogui.hotkey('alt', 'right')
        print('prev,')
        time.sleep(0.1)
    elif pred == 1: # fast_forward
        # pyautogui.hotkey('right')
        print('double prev,')
        time.sleep(0.1)
    elif pred == 2: # forward
        # pyautogui.hotkey('left')
        print('doublenext')
        time.sleep(0.1)
    elif pred == 3:
        # pyautogui.hotkey('alt', 'left')
        print('next')
        time.sleep(0.1)