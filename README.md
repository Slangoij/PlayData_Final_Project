# PlayData_Final_Project
핸드모션을 이용한 윈도우 컨트롤러_플레이데이터 최종 프로젝트

## 1. 프로젝트 목적, 기획배경
- 데스크탑을 사용하면서 멀리서도 이를 제어하고 싶다는 아이디어로, 웹캠을 이용하여 제어하는 것은 어떨까 제안.

## 2. 예상 기술 스택 및 모델 구조
![image](https://user-images.githubusercontent.com/71580318/123107686-b8673b00-d474-11eb-8ed6-2a24b6cd1d71.png)

## 3. 디렉토리 구조
```bash
├── common                  - model, src에 공통으로 쓰이는 module
│   ├── draw                - img 데이터 생성, 데이터 저장
│   └── HandTrackingModule  - 손 인식 모듈
│
├── model
│   ├── data
│   │    ├── csv            - 비정제, 정제, temp (-> 추론 데이터)
│   │    └── img            - 비정제, 정제, temp (-> 추론 데이터)
│   ├── process             - 각 모델별(VGG, MobilNetV2, LSTM) 생성 파일
│   ├── saved_model         - 학습된 모델 저장 directory
│   └── preprocessing.py    - 학습 데이터 생성 file
│
├── src
    ├── test                - test를 위한 directory
    ├── user_interface      - GUI user interface
    ├── AutopyClass.py      - window controller
    └── model_preprocess.py - 모델 input 값 전처리, 추론 함수 정의
```

## 4. 예상 결과물
![2021-06-23 22;23;57](https://user-images.githubusercontent.com/71580318/123104237-ba7bca80-d471-11eb-86de-1765494aaff0.PNG)
  
  
## 5. 참고 자료
- [virtual painter](https://www.youtube.com/watch?v=ZiwZaAVbXQo)
- [Real-Time Hand Gesture 논문](https://www.koreascience.or.kr/article/JAKO201919866854640.pdf)
