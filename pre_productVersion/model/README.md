# Model
- VGG16
- MobileNetV2
- LSTM

## MobileNetV2 디렉토리 경로
```bash
├── data/
│   ├── original/           - 원본 경로
│   │   ├── backward    
│   │   ├── fast_forward
│   │   └── forward
│   ├── backward            - 증강된 데이터
│   ├── fast_forward
│   └── forward
├── train/                  - 모델 학습
│   ├── backward
│   ├── fast_forward
│   └── forward
└── test/                   - 모델 검증 및 평가
    ├── backward
    ├── fast_forward
    └── forward 
```

####################################################
# 여기서 부터 새로 수정

## 디렉토리 경로
```bash
├── data/
│   ├── csv/           
│   │   ├── 비정제데이터    
│   │   ├── 정제데이터
│   │   └── temp
│   └── img/
│       ├── 비정제데이터    
│       ├── 정제데이터
│       └── temp
│
├── train/                  - 모델 학습
│   ├── backward
│   ├── fast_forward
│   └── forward
└── test/                   - 모델 검증 및 평가
    ├── backward
    ├── fast_forward
    └── forward 
```

## date directory
- 학습을 위한 데이터 directory
- 이전 비정제 데이터와 정제 데이터 보관
- temp == 앞으로 새로 생기는 데이터 저장 directory

## process
- 각 모델 구축 과정 ipy note file
- colab에서 진행

## saved_model
- 학습 후 저장된 모델 파일

## preprocessing file
- 학습용 데이터 생성 파일