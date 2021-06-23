# PlayData_Final_Project
핸드모션을 이용한 윈도우 컨트롤러_플레이데이터 최종 프로젝트

# 1. 프로젝트 목적, 기획배경
- 데스크탑을 사용하면서 멀리서도 이를 제어하고 싶다는 아이디어로, 웹캠을 이용하여 제어하는 것은 어떨까 제안.

# 2. 예상 기술 스택 및 모델 구조
![image](https://user-images.githubusercontent.com/71580318/123107686-b8673b00-d474-11eb-8ed6-2a24b6cd1d71.png)

# 3. 디렉토리 구조
```bash
├── inputdata_preprocessing - 모델 학습 관련 데이터
│   ├── image               - 학습용 이미지 데이터 원본 경로
│   │   ├── img_class       - 클래스별 분류된 이미지 디렉토리    
│   │   └── ...
│   ├── model               - 학습 모델
│   │   └── fast_forward
│   └── preprocessing.py    - 이미지 전처리 모듈
├── model                   - 사전 학습 모델
│   ├── vgg_model           - vgg 모델
│   ├── mobilenet_model     - mobilenet 모델
│   └── ...
└── user_interface          - GUI 모듈
    ├── xxx.py
    └── ...
```

# 5. 예상 결과물
![2021-06-23 22;23;57](https://user-images.githubusercontent.com/71580318/123104237-ba7bca80-d471-11eb-86de-1765494aaff0.PNG)
  
  
## 참고 자료1
- [virtual painter](https://www.youtube.com/watch?v=ZiwZaAVbXQo)
- [Real-Time Hand Gesture 논문](https://www.koreascience.or.kr/article/JAKO201919866854640.pdf)
