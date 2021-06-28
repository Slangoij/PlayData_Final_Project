import sys
import pyautogui
import time
import datetime
import cv2

def window_controller(pred):
    # 유튜브 모드
    control_list = ['l', 'j', 'k', 'f']
    # j : 10초 이전, l : 10초 이후, k : 일시정지 / 재생, f : 전체화면 / 원상복구
    command = control_list[pred]
    pyautogui.press(command)