import sys
import pyautogui
import time
import datetime
import cv2

def window_controller(pred):
    if pred == 0: # backward
        # pyautogui.keyDown('ctrl')
        # time.sleep(0.1)
        # pyautogui.keyUp('')
        pyautogui.hotkey('alt', 'left')
    elif pred == 1: # fast_forward
        pyautogui.hotkey('right')
    elif pred == 2: # forward
        pyautogui.hotkey('alt', 'right')
    else:
        pass