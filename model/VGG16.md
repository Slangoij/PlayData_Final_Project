```python
from google.colab import drive
drive.mount('/content/drive')
```

# 깃헙 동기화 및 경로 설정
```python
%cd /content/drive/MyDrive/Final_project
!git clone https://github.com/Slangoij/PlayData_Final_Project.git
%cd /content/drive/MyDrive/Final_project/PlayData_Final_Project
```

# 하이퍼파라미터 및 데이터 경로 설정
```python
import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.applications import VGG16, ResNet50V2, MobileNetV2
from tensorflow.keras.preprocessing.image import ImageDataGenerator

# 하이퍼 파라미터
LEARNING_RATE = 0.001
N_EPOCHS = 20
N_BATCHS = 20
NUM_CLASSES = 3 # 클래스 개수
CLASS_MODE = 'categorical'
INPUT_SHAPE = (640, 480, 3) # 학습할 이미지 shape
FEATURE_SHAPE = (20, 15, 512) # 모델에 맞춰 변경해야 한다!

# 학습데이터 및 모델 경로 설정
train_dir = './inputdata_preprocessing/classedImg/train'
validation_dir = './inputdata_preprocessing/classedImg/val'
test_dir = './inputdata_preprocessing/classedImg/test'
MODEL_PATH = './model/vgg16'
```

# 함수: 데이터 증강, 특성 추출, 분류기 모델 생성
```python
# 데이터 증강
def get_generators():
    '''
    train, validation, test generator를 생성해서 반환.
    train generator는 image 변환 처리
    '''
    # 상하좌우 이동, 확대, 회전 이미지로 증강
    train_datagen = ImageDataGenerator(rescale=1/255,
                                       rotation_range=20,
                                       zoom_range=0.5,
                                       height_shift_range=0.3,
                                       width_shift_range=0.3)
    
    test_datagen = ImageDataGenerator(rescale=1/255) #validation/test에서 사용

    # generator 들 생성
    # 첫번째는 먼저 한동작이므로 동작과 비동작으로 바이너리 구분만
    train_generator = train_datagen.flow_from_directory(train_dir,
                                                        target_size=INPUT_SHAPE[:2],
                                                        batch_size=N_BATCHS,
                                                        class_mode=CLASS_MODE)    
    val_generator = test_datagen.flow_from_directory(validation_dir,
                                                     target_size=INPUT_SHAPE[:2],
                                                     batch_size=N_BATCHS,
                                                     class_mode=CLASS_MODE)
    test_generator = test_datagen.flow_from_directory(test_dir,
                                                      target_size=INPUT_SHAPE[:2],
                                                      batch_size=N_BATCHS,
                                                      class_mode=CLASS_MODE)
    return train_generator, val_generator, test_generator


# 특성 추출로 빠른 학습
def extract_featuremap(image_directory, sample_counts):
  """
  매개변수로 받은 디렉토리의 이미지를 Conv_base(VGG16) 모델을 통과시켜 Featuremap을 추출해 반환하는 함수
  [매개변수]
    image_directory: 이미지 데이터들이 있는 디렉토리
    sample_counts: 특성을 추출할 이미지 개수
  [반환값]
    튜플: (featuremap들, label)
  """
  conv_base = VGG16(weights='imagenet', include_top=False, input_shape=INPUT_SHAPE)

  # 결과를 담을 ndarray
  return_features = np.zeros(shape=(sample_counts, 20, 15, 512)) # Featuremap저장, conv_base의 마지막 layer의 output의 shape에 맞춘다.
  return_labels = np.zeros(shape=(sample_counts,NUM_CLASSES)) # label 저장

  datagen = ImageDataGenerator(rescale=1./255)
  iterator = datagen.flow_from_directory(image_directory,
                                         target_size=INPUT_SHAPE[:2],
                                         batch_size=N_BATCHS,
                                         class_mode=CLASS_MODE)
  i = 0 # 반복횟수 저장할 변수
  for input_batch, label_batch in iterator: # (image, label) * batch크기(100)
    # input_batch를 conv_base 넣어서 featuremap을 추출
    fm = conv_base.predict(input_batch)

    return_features[i*N_BATCHS: (i+1)*N_BATCHS] = fm
    return_labels[i*N_BATCHS: (i+1)*N_BATCHS] = label_batch

    i+=1
    if i*N_BATCHS >= sample_counts: # 결과를 저장할 배열의 시작index가 sample_counts보다 크면 반복문 멈추기
      break

  return return_features, return_labels


def create_model():
  # 분류기 모델만 생성
  model = keras.Sequential()
  model.add(layers.Input(FEATURE_SHAPE))
  model.add(layers.GlobalAveragePooling2D())
  model.add(layers.Dropout(rate=0.5))
  model.add(layers.Dense(256, activation='relu'))
  model.add(layers.BatchNormalization())
  model.add(layers.Dense(NUM_CLASSES, activation='softmax'))

  return model

# 결과 출력
def plot_result(history, ymin=None, ymax=None):
    plt.figure(figsize=(15,5))
    plt.subplot(1,2,1)

    plt.plot(range(1,N_EPOCHS+1), history.history['loss'], label='train loss')
    plt.plot(range(1,N_EPOCHS+1), history.history['val_loss'], label='validation loss')
    plt.title('LOSS')
    plt.xlabel('Epochs')
    plt.ylabel('Loss')
    if ymin!=None and ymax!=None:
        plt.ylim(ymin, ymax)
    plt.legend()

    plt.subplot(1,2,2)
    plt.plot(range(1, N_EPOCHS+1), history.history['accuracy'], label='train accuracy')
    plt.plot(range(1, N_EPOCHS+1), history.history['val_accuracy'], label='validation accuracy')
    plt.title('ACCURACY')
    plt.xlabel('Epochs')
    plt.ylabel('Accuracy')
    if ymin!=None and ymax!=None:
        plt.ylim(ymin, ymax)
    plt.legend()

    plt.tight_layout()
    plt.show()
```

# 학습 이미지 정리(디렉토리, 이름, 파일 개수)
```python
import shutil
# 기존 데이터 디렉토리 지우기
# shutil.rmtree(train_dir, ignore_errors=True)
# shutil.rmtree(validation_dir, ignore_errors=True)
# shutil.rmtree(test_dir, ignore_errors=True)

import os
import random

os.makedirs(train_dir, exist_ok=True)
os.makedirs(validation_dir, exist_ok=True)
os.makedirs(test_dir, exist_ok=True)

ORG_IMG_PATH = "./inputdata_preprocessing/img"
img_file_list = os.listdir(ORG_IMG_PATH)

for i in range(len(img_file_list)):
  train_under_dir = train_dir + '/' + str(i) + '/'
  validation_under_dir = validation_dir + '/' + str(i) + '/'
  test_under_dir = test_dir + '/' + str(i) + '/'
  
  os.makedirs(train_under_dir, exist_ok=True)
  os.makedirs(validation_under_dir, exist_ok=True)
  os.makedirs(test_under_dir, exist_ok=True)

  tmp_img_path = os.path.join(ORG_IMG_PATH, img_file_list[i])
  img_list = os.listdir(tmp_img_path)
  train_len = int(len(img_list)*0.7) # 70%를 train으로 넣어줌
  val_len = int(len(img_list)*0.9) # 나머지 20%를 train으로 넣어줌 나머지는 test
  random.shuffle(img_list)

  count = 0
  for img_name in img_list:
      if count < train_len:
          shutil.copy(tmp_img_path + '/' + img_name, train_dir + '/' + str(i) + '/' + img_name) # 이미지 copy
      elif count < val_len:
        shutil.copy(tmp_img_path + '/' + img_name, validation_dir + '/' + str(i) + '/' + img_name)
      else:
        shutil.copy(tmp_img_path + '/' + img_name, test_dir + '/' + str(i) + '/' + img_name)
      count += 1
```

# 메인 작업(모델 학습)
```python
# train, val, test 각 폴더 내 데이터 개수
data_cnts = []
for dirs in [train_dir, validation_dir, test_dir]:
  cnt = 0
  for (path, dir, files) in os.walk(dirs):
    cnt += len(files)
  data_cnts.append(cnt)

# Featuremap 추출
train_features, train_labels = extract_featuremap(train_dir, data_cnts[0])
validation_features, validation_labels = extract_featuremap(validation_dir, data_cnts[1])
test_features, test_labels = extract_featuremap(test_dir, data_cnts[2])

mc_callback = keras.callbacks.ModelCheckpoint(MODEL_PATH, monitor='val_loss', save_best_only=True)

train_iterator, validation_iterator, test_iterator = get_generators()

model = create_model()
model.compile(optimizer=keras.optimizers.Adam(learning_rate=LEARNING_RATE), 
              loss='categorical_crossentropy', # 클래스 따라 변경
              metrics=['accuracy'])
model.summary()

# 특성 추출 없이
# history = model.fit(train_iterator, epochs=N_EPOCHS,
#                     steps_per_epoch=len(train_iterator),
#                     validation_data=validation_iterator,
#                     validation_steps=len(validation_iterator),
#                     callbacks=[mc_callback])

# 특성 추출해서
history = model.fit(train_features, train_labels,
                    epochs=N_EPOCHS,
                    validation_data=(validation_features, validation_labels),
                    batch_size=N_BATCHS,
                    callbacks=[mc_callback])

best_model = keras.models.load_model(MODEL_PATH)
```

# 모델 평가
```python
# 모델 합치기
whole_model = keras.Sequential()
whole_model.add(VGG16(weights='imagenet', include_top=False, input_shape=INPUT_SHAPE))
whole_model.add(best_model)
whole_model.compile(optimizer=keras.optimizers.Adam(learning_rate=LEARNING_RATE), 
              loss='binary_crossentropy', # 클래스 따라 변경
              metrics=['accuracy'])
whole_model.summary()

# evaluation
whole_model.evaluate(train_iterator)
whole_model.evaluate(test_iterator)
```
