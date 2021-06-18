```python
#@title Categorical_MobileNetV2.md
#@markdown colab 사용
from google.colab import drive
drive.mount('/content/gdrive/')
```


```python
# library import
import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.preprocessing.image import load_img, img_to_array
# load_img 함수: 이미지 불러오기
# img_to_array함수 : 불러온 이미지를 numpy 배열 (ndarray)로 변환
# local에서 사용하려면 Pillow를 설치해야 한다. (pip install Pillow)

# Extract features
import os
import shutil
from os import rename, listdir
from keras.preprocessing.image import ImageDataGenerator
# split data
from sklearn.model_selection import train_test_split
import re
import random
import xml.etree.ElementTree as et
from PIL import Image
 
import cv2 
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle # 바운딩 박스를 그림

 # import the necessary packages
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
from tensorflow.keras.layers import AveragePooling2D
from tensorflow.keras.layers import Dropout, Flatten, Dense, Input, Model
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.utils import to_categorical
from sklearn.preprocessing import LabelBinarizer
from sklearn.metrics import classification_report
from imutils import paths
import matplotlib.pyplot as plt
import argparse

# print(tf.__version__)
# print(keras.__version__)
np.random.seed(1)
tf.random.set_seed(1)
```


```python
# 파이썬 매직코드
!pwd
```


```python
# 리눅스 코드
# 경로 설정
%cd /content/gdrive/My\ Drive/final_project
```


```python
#@markdown 현재 경로
os.getcwd()
```


```python
PATH = "./data"

img_file_list = os.listdir(PATH) # IMAGE_PATH에 있는 파일/폴더명 조회
print(len(img_file_list))
print(img_file_list)
print(os.listdir('./data/original'))
print(os.listdir('./data/original/fast_forward'))
```


```python
# 직선의 경우 기울기를 많이 돌려야 하지 않아야 해서 3로 설정
# https://keras.io/api/preprocessing/image/#imagedatagenerator
# https://ysyblog.tistory.com/152
# https://tykimos.github.io/2017/06/10/CNN_Data_Augmentation/
ORIGINAL_PATH = './data/original/'
for p in os.listdir(ORIGINAL_PATH):
    PATH = p

    data_datagen = ImageDataGenerator(rescale=1./255,
                                    rotation_range=3, # 지정된 각도 범위 내에서 임의로 원본 이미지 회전
                                    width_shift_range=0.1,
                                    height_shift_range=0.1,
                                    zoom_range = 0.1,
                                    fill_mode='nearest') 
    filename_in_dir = [] 
    target_path = ORIGINAL_PATH + p
    for root, dirs, files in os.walk(target_path):
        for  fname in files:
            full_fname = os.path.join(root, fname)
            filename_in_dir.append(full_fname)

    target_image_list = [fname for fname in filename_in_dir if os.path.splitext(fname)[-1]=='.png']
    for file_image in target_image_list:
        img = load_img(file_image)
        x = img_to_array(img)
        x = x.reshape((1,) + x.shape)
    
        i = 0
    
        for batch in data_datagen.flow(x,save_to_dir='./data/'+p, save_prefix='changed', save_format='png'):
            i += 1
            if i > 300: # if i > 100: 이 부분으로 증가시킬 양을 결정할 수 있다.
                break
```


```python
# img의 상태 파악
img = cv2.imread('./data/forward/changed_0_0.png', cv2.IMREAD_UNCHANGED)
print("Image Size : ",img.size)
print("Image Shape : ",img.shape)
print("Image Data Type : ", img.dtype)
```


```python
data_path = [f for f in os.listdir('./data') if f != 'original']
print(data_path)
```


```python
!pwd
```


```python
# 데이터 분리, move or copy 사용
FORWARD_PATH = './data/forward'
FAST_FORWARD_PATH= './data/fast_forward'
BACKWARD_PATH = './data/backward'
forward_list = os.listdir(FORWARD_PATH)
fast_forward_list = os.listdir(FAST_FORWARD_PATH)
backward_list = os.listdir(BACKWARD_PATH)
```


```python
print(backward_list)
```


```python
def copy_to_train(img_list, train_path, test_path, label):
    count = 0
    current_label = None
    train_len = int(len(img_list)*0.7)
    random.shuffle(img_list)

    for img_name in img_list:
        # label = img_list.split('_')[0]
        if current_label != label: # 새로운 라벨 카피 시작
            count = 0
            current_label = label

        if label == 'forward':
            pa = FORWARD_PATH + '/'
            th = '/forward/'
        elif label == 'fast':
            pa = FAST_FORWARD_PATH + '/'
            th = '/fast_forward/'
        elif label == 'backward':
            pa = BACKWARD_PATH + '/'
            th = '/backward/'

        # count가 train_len다 작으면 train 폴더에 copy, 이상이면 test 폴더에 copy
        if count < train_len:
            shutil.copy(pa + img_name, train_path + th) # 이미지 copy
            # train_path를 train_path + th + img_name로 바꿔도 동일하다
        else:
            shutil.copy(pa + img_name, test_path + th)

        count += 1
```


```python
# category별로 -> train과 test로 분리
copy_to_train(forward_list,"./train",'./test','forward')
copy_to_train(fast_forward_list,"./train",'./test','fast')
copy_to_train(backward_list,"./train",'./test','backward')
```


```python
LEARNING_RATE = 0.0002
N_EPOCHS = 30
N_BATCHS = 200 # N_BATCHS = 100
IMAGE_SIZE = 224
N_CLASS = 3
DROPOUT_RATE = 0.3
```


```python
# 학습데이터 및 모델 경로 설정
train_dir = './train'
validation_dir = './test'

# generator 생성
def get_generators():
    '''
    train, validation, test generator를 생성해서 반환.
    train generator는 image 변환 처리
    '''
    train_datagen = ImageDataGenerator(rescale=1/255,
                                       brightness_range=(0.8,1.2))
    test_datagen = ImageDataGenerator(rescale=1/255)

    # generator 들 생성
    train_generator = train_datagen.flow_from_directory(train_dir,
                                                        target_size=(224,224),
                                                        batch_size=N_BATCHS,
                                                        class_mode='categorical')    
    val_generator = test_datagen.flow_from_directory(validation_dir,
                                                        target_size=(224,224),
                                                        batch_size=N_BATCHS,
                                                        class_mode='categorical')
    return train_generator, val_generator
```


```python
# MobileNetV2 기반으로 실행
conv_base = MobileNetV2(weights="imagenet",
                        include_top=False,
                        input_tensor=Input(shape=(224,224,3))
                        )
```


```python
from tensorflow.keras import layers

def create_model():
    conv_base = MobileNetV2(weights="imagenet", include_top=False, input_tensor=Input(shape=(224,224,3)))
    conv_base.trainable = False # 학습시 weight 최적화(update)를 하지 않도록 설정. => 모델 컴파일 전에 실행

    model = keras.Sequential()
    model.add(conv_base)
    model.add(layers.GlobalAveragePooling2D())
    model.add(layers.Dense(256, activation='relu'))
    model.add(layers.BatchNormalization()) # << 찾아보기
    model.add(layers.Dense(128, activation='relu'))
    model.add(layers.Dropout(rate=0.5))

    # 출력
    model.add(layers.Dense(N_CLASS, activation='softmax'))

    return model
```


```python
model = create_model()
model.compile(optimizer=keras.optimizers.Adam(learning_rate=LEARNING_RATE),
              loss='categorical_crossentropy', metrics=['accuracy'])
model.summary()
```


```python
train_iterator, validation_iterator = get_generators()
```


```python
h_callback = keras.callbacks.ModelCheckpoint('./models', monitor='val_loss', save_best_only=True)

history = model.fit(train_iterator,
                    epochs=N_EPOCHS,
                    steps_per_epoch=len(train_iterator),
                    validation_data=validation_iterator,
                    validation_steps=len(validation_iterator),
                    callbacks=[h_callback])
```


```python
# plot the training loss and accuracy
N = N_EPOCHS
plt.style.use("ggplot")
plt.figure()
plt.plot(np.arange(0, N), history.history["loss"], label="train_loss")
plt.plot(np.arange(0, N), history.history["val_loss"], label="val_loss")
plt.plot(np.arange(0, N), history.history["accuracy"], label="train_acc")
plt.plot(np.arange(0, N), history.history["val_accuracy"], label="val_acc")
plt.title("Training Loss and Accuracy")
plt.xlabel("Epoch #")
plt.ylabel("Loss/Accuracy")
plt.legend(loc="lower left")
```


```python
model.save("my_model.h5")
```


```python
# 모델 predict
import imutils # opencv의 부족한 점을 채워준다 머시기..
from google.colab.patches import cv2_imshow # colab에서 쓸 수 있는 imshow
# img_path = './final/roll2.png'
img_path = './final/forward4.png'
# img_path = './final/backward1.png'
img = load_img(img_path, target_size=(224,224)) # target_size를 지정 : 읽어올 때 resize처리한다.

# ndarray 변환
sample = img_to_array(img)

# batch크기 축(0번 축) 늘리기
sample_x = sample[np.newaxis, ...]
sample_x = sample_x/255.

```


```python
pred  = model.predict(sample_x)
print(pred)
# 추론
# 0 : backward 1 : fast_forward 2 : forward
pred_class = np.argmax(pred, axis=-1)
print(pred_class)
```


```python
image = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
cv2_imshow(image)
cv2.waitKey(0)
```
