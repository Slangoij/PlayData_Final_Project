import sys
import pyautogui
import time
import datetime
import cv2

def window_controller(pred):
    if pred == 0: # backward
        # pyautogui.hotkey('alt', 'right')
        print('next')
        time.sleep(0.1)
    elif pred == 1: # fast_forward
        # pyautogui.hotkey('right')
        print('prev')
        time.sleep(0.1)
    elif pred == 2: # forward
        # pyautogui.hotkey('left')
        print('s')
        time.sleep(0.1)
    elif pred == 3:
        # pyautogui.hotkey('alt', 'left')
        print('w')
        time.sleep(0.1)