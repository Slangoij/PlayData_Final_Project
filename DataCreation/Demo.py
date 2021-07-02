import HandTrackingModule as htm
import GestureModelModule as gmm
import AutopyClass
from tensorflow import keras
import numpy as np
import cv2
import draw
# from src.user_interface.webcam import DryHand as dr
    
class demopy():
    def __init__(self):
        ###########################################
        # 모델 추론시 변수 초기 셋팅
        self.draw_arr = []
        self.in_check = 0
        self.out_check = 0
        self.control_mode = False
        self.model_selection = 'CNN'
        self.conf_limit = 0.80
        self.hCam, self.wCam = 640, 640
        self.num = 0
        self.confidence = 0
        self.detector = htm.handDetector(maxHands=1, detectionCon=0.75)
        self.gesture_model = keras.models.load_model('C:\\Users\\mein0\\01_testFinal\\deployment01\\model\\vgg16_model_4cls_ws_id_2-3_noangle.h5')
        ###########################################

    def predict(self, img):
        # 손 인식시
        img = self.detector.findHands(img)
        self.landmark_list, bbox = self.detector.findPosition(img, draw=False)
        action = ''
 
        imgCanvas = None
        if self.landmark_list:
            self.out_check = 0
            self.fingers = self.detector.fingersUp()
            if 1 not in self.fingers[1:]:
                # 주먹 쥐면 검지의 좌표 저장
                self.in_check += 1
                if self.in_check == 10:
                    self.in_check = 0
                    self.control_mode = True        
            if self.control_mode:
                self.draw_arr.append(self.landmark_list[8][1:])
                cv2.circle(img, tuple(self.landmark_list[8][1:]), 7, (255,0,0), cv2.FILLED)
        else:
            self.out_check += 1
            if self.out_check == 10 and self.control_mode:
                self.control_mode = False
                if not self.control_mode:
                    if 20 < len(self.draw_arr) <= 100:
                        # 저장한 좌표로 input 데이터 생성
                        # 모델 추론
                        self.draw_arr = self.draw_arr[10:-7] # 앞, 뒤 10 frame 씩 제외 ## -5
                        input_data, imgCanvas = gmm.trans_input(self.draw_arr, self.wCam, self.hCam, self.model_selection)
                        pred, self.confidence = gmm.predict(self.gesture_model, input_data)
                        
                        self.num = draw.save_file(imgCanvas, self.draw_arr)
                        # if self.confidence > self.conf_limit:
                            # action = AutopyClass.window_controller(pred)
  
                        # Canvas = np.zeros((self.wCam, self.hCam, 3), np.uint8)
                    self.draw_arr.clear()

        return self.control_mode, str(self.num), self.confidence, imgCanvas