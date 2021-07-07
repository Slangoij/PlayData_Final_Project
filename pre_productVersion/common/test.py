import pandas as pd
import datetime
import os
import cv2
import logging

def draw_canvas(img, cnt, draw_arr):
    '''
    전달 받은 좌표 arr로 이미지 데이터 생성
    '''
    prev_index = tuple(draw_arr[0])
    for i in range(1, cnt):
        # 이전, 현재 좌표 저장하여 선 연결
        curr_index = tuple(draw_arr[i])
        cv2.line(img, prev_index, curr_index, (255, 255, 255), 7)
        prev_index = curr_index
    return img

def save_file(Canvas, draw_arr, img_path, csv_path=None, pred=None):
    '''
    모델이 예측한 라벨로 데이터 저장
        차후 학습 데이터로 사용
    '''
    base_path = img_path
    labels = os.listdir(base_path) # ['01next', '02previous', '03S', '04W']
    label = 'None'
    # pred가 숫자로 되어있으면 path 추가
    if pred:
        label = labels[pred]
        img_path = os.path.join(img_path, label)
        csv_path = os.path.join(csv_path, label)

    t = datetime.datetime.now().strftime('%Y-%m-%d %H-%M-%S')
    # 이미지 파일 저장
    cv2.imwrite(os.path.join(img_path, f'{t}.png'), Canvas)
    print(f'save {label} img')
    # logging.info(f'save {label} img')
    # csv 파일 저장
    if csv_path:
        df = pd.DataFrame(draw_arr)
        df.to_csv(os.path.join(csv_path, f'{t}.csv'), header=False, index=False)
        # print(f'save {label} csv')
        # logging.info(f'save {label} csv')