import pandas as pd
import datetime
import os
import cv2

def draw_canvas(img, frame_cnt, draw_arr):
    '''
    전달 받은 좌표 arr로 이미지 데이터 생성
    input_parameter:
        img: opencv에서 받아온 이미지
        frame_cnt: 동영상frame 개수
        draw_arr: 검지의 좌표 list
    반환값:
        img: 캔버스에 궤적을 그린 이미지
    '''
    prev_index = tuple(draw_arr[0])
    for i in range(1, frame_cnt):
        # 이전, 현재 좌표 저장하여 선 연결
        curr_index = tuple(draw_arr[i])
        cv2.line(img, prev_index, curr_index, (255, 255, 255), 7)
        prev_index = curr_index
    return img

# def save_file(Canvas, draw_arr, pred=None):
#     img_path = './model/data/img/temp'
#     csv_path = './model/data/csv/temp'
#     data_path = './model/data/img/temp'
#     '''
#     if label:
#         모델이 예측한 라벨로 데이터 저장
#         차후 학습 데이터로 사용
    
#     input_data:
#         Canvas: 손동작 궤적을 그린 이미지
#         draw_arr: 검지의 좌표 list
#         pred: 손동작 라벨
#     '''
#     labels = os.listdir(data_path)
#     if pred < len(labels):
#         label = labels[pred]
#         img_path = os.path.join(img_path, label)
#         csv_path = os.path.join(csv_path, label)
    
#     t = datetime.datetime.now().strftime('%Y-%m-%d %H-%M-%S')
#     # 이미지 파일 저장
#     cv2.imwrite(os.path.join(img_path, f'{t}.png'), Canvas)
#     # csv 파일 저장
#     df = pd.DataFrame(draw_arr)
#     df.to_csv(os.path.join(csv_path, f'{t}.csv'), header=False, index=False)

def save_file(Canvas, draw_arr):
    img_path = './img/'
    csv_path = './csv/'  

    t = datetime.datetime.now().strftime('%Y-%m-%d %H-%M-%S')
    # 이미지 파일 저장
    cv2.imwrite(os.path.join(img_path, f'Young{t}.png'), Canvas)
    # csv 파일 저장
    df = pd.DataFrame(draw_arr)
    df.to_csv(os.path.join(csv_path, f'Young{t}.csv'), header=False, index=False)
