from common import HandTrackingModule as htm
from src import gmm as gmm
from src import AutopyClass
from tensorflow import keras
from common import draw
import numpy as np
import cv2
#####################################
# webcam size 지정
hCam, wCam = 640, 640
# model 설정 값 초기 정의
model_name = 'vgg16_model_4cls_ws_id_2-3_noangle'
model_selection = 'CNN'
conf_limit = 0.75
#####################################

# pre-train된 모델 로드
gesture_model = keras.models.load_model(r'./././model/saved_model/{0}.h5'.format(model_name))
detector = htm.handDetector(maxHands=1, detectionCon=0.75)


cap = cv2.VideoCapture(0)
# webcam size 조정
cap.set(3, wCam)
cap.set(4, hCam)

draw_arr = []
in_check = 0
out_check = 0
control_mode = False

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)
    
    # 이미지에서 손인식
    img = detector.findHands(img)
    landmark_list, bbox = detector.findPosition(img, draw=False)

    # 손 인식 되면
    if landmark_list:
        out_check = 0
        fingers = detector.fingersUp()
        if 1 not in fingers[1:]:
            # 주먹 쥐면 검지의 좌표 저장
            in_check += 1
            if in_check == 10:
                in_check = 0
                control_mode = True
        if control_mode:
            draw_arr.append(landmark_list[8][1:])
            cv2.circle(img, tuple(landmark_list[8][1:]), 7, (255,0,0), cv2.FILLED)
    else:
        # 손 인식 안되면
        out_check += 1
        if out_check == 10 and control_mode:
            control_mode = False
            if not control_mode:
                if 20 < len(draw_arr) <= 100:
                    # 저장한 좌표로 input 데이터 생성
                    # 모델 추론
                    draw_arr = draw_arr[10:-10] # 앞, 뒤 10 frame 씩 제외
                    input_data, imgCanvas = gmm.trans_input(draw_arr, wCam, hCam, model_selection)
                    pred, confidence = gmm.predict(gesture_model, input_data)
                    
                    # 예측률 75% 이상 input 데이터 저장
                    if confidence > conf_limit:
                        AutopyClass.window_controller(pred)
                        draw.save_file(imgCanvas, draw_arr, pred)
                    Canvas = np.zeros((wCam, hCam, 3), np.uint8)
                draw_arr.clear()

    cv2.imshow('img', img)
    cv2.waitKey(1)

