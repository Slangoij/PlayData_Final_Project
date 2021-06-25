# draw Module
## 함수 정리
- `draw_canvas`
    - 전달 받은 좌표로 이미지 데이터 생성

    ![image](https://user-images.githubusercontent.com/77317312/123464344-a5489c80-d627-11eb-80ab-05751f91d1d6.png)
- `save_file`
    - image 파일 혹은 csv 파일을 저장해주는 모듈
    - 모델이 예측한 예측률이 75% 이상이면 예측한 라벨의 디렉토리로 저장
    - 파일명이 중복되는 것을 방지하기 위해 현재 날짜와 시간(초)으로 파일명 저장