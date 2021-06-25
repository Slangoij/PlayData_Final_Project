import pandas as pd
import datetime
import os
import cv2

def draw_canvas(img, cnt, draw_arr):
    # 검지
    prev_index = tuple(draw_arr[0])
    for i in range(1, cnt):
        # 검지
        curr_index = tuple(draw_arr[i])
        cv2.line(img, prev_index, curr_index, (255, 255, 255), 7)
        prev_index = curr_index
    return img

def save_file(Canvas, draw_arr, img_path, csv_path):
    t = datetime.datetime.now().strftime('%Y-%m-%d %H-%M-%S')
    cv2.imwrite(os.path.join(img_path, f'{t}.png'), Canvas)

    df = pd.DataFrame(draw_arr)
    df.to_csv(os.path.join(csv_path, f'{t}.csv'), header=False, index=False)
