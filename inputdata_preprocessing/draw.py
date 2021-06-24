import datetime
import os
import cv2

def draw_canvas(img, cnt, draw_arr):
    # 검지
    prev_index = tuple(draw_arr[0][:2])
    for i in range(1, cnt):
        # 검지
        curr_index = tuple(draw_arr[i][:2])
        cv2.line(img, prev_index, curr_index, (255, 255, 255), 7)
        prev_index = curr_index

    return img

def save_image_file(Canvas, path):
    t = datetime.datetime.now().strftime('%Y-%m-%d %h-%M-%S')
    cv2.imwrite(os.path.join(path, f'{t}.png'), Canvas)
