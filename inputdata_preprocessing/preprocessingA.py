import numpy as np
import cv2
import HandTrackingModule as htm
import os
import time
import datetime
import pandas as pd
import draw
####################################################################
# webcam 화면 사이즈 조정 파라미터
wCam, hCam = 640, 360
####################################################################

detector = htm.handDetector(detectionCon=0.75, maxHands=1)

cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)

# model input값 초기화 이하 Canvas
Canvas = np.zeros((hCam, wCam, 3), np.uint8)
csv_arr = []  # frame 저장 변수
draw_arr = []
frame_limit = 20
########
prev_time = 0
FPS = 30
########

<<<<<<< HEAD
img_path = '/img'
=======
img_path = 'img'
>>>>>>> develop
csv_path = 'csv'

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)

    img = detector.findHands(img)
    landmark_list, bbox = detector.findPosition(img, draw=False)
    if landmark_list:
        fingers = detector.fingersUp()

    curr_time = time.time() - prev_time
    # 초당 프레임수 제한.
    if (success is True) and (curr_time > 1. / FPS):
        prev_time = time.time()

        # 손 인식 되면 csv_arr에 넣기
        if len(landmark_list):
            # 손을 다 폈을 때와 검지만 폈을 때 구분
            if fingers[1] and fingers[4]:
                two_fingers = landmark_list[8][1:] + landmark_list[20][1:]
<<<<<<< HEAD
                input_arr.append(two_fingers)
                print(input_arr[0])
            elif fingers[1]:
                input_arr.append(landmark_list[8][1:])
            # input_arr 길이가 frame_이면  Canvas에 그리기
            if len(input_arr) == frame_limit:
                Canvas = draw.draw_canvas(Canvas, frame_limit, input_arr)
=======
                csv_arr.append(two_fingers)
                draw_arr.append(two_fingers)
            elif fingers[1]:
                csv_arr.append(landmark_list[8][1:] + [0, 0])
                draw_arr.append(landmark_list[8][1:])
            # csv_arr 길이가 frame_이면  Canvas에 그리기
            if len(draw_arr) == frame_limit:
                Canvas = draw.draw_canvas(Canvas, frame_limit, draw_arr)
>>>>>>> develop
                # output값을 보기 위한 png파일 변환
                t = datetime.datetime.now().strftime("%Y-%m-%d %H-%M-%S")
                df = pd.DataFrame(csv_arr)
                df.to_csv(os.path.join(csv_path, f'{t}.csv'), index=False, header=False)

                cv2.imwrite(os.path.join(img_path, f'{t}.png'), Canvas)
                Canvas = np.zeros((hCam, wCam, 3), np.uint8)  # Canvas 초기화
                # 먼저 들어온 데이터 빼기
                csv_arr = csv_arr[10:]
                draw_arr = draw_arr[10:]
        # 손 인식이 안되면 clear
        else:
            csv_arr.clear()
            draw_arr.clear()


    cv2.imshow('img', img)
    if cv2.waitKey(1) == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()


