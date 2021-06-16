import pyautogui
import time
import datetime


def enterCommand(command):
    if len(command)>1:
        for i in command:
            pyautogui.keyDown(i)
            time.sleep(0.1)
        for t in reversed(command):
            pyautogui.keyUp(t)
            time.sleep(0.1)

    else:
        pyautogui.press(command)

