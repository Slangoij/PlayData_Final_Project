# Model
- VGG16
- MobileNetV2

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