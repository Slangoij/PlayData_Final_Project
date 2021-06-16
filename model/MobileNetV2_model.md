```python
from google.colab import drive
drive.mount('/content/gdrive/')
```


```python
# 데이터 증강 모듈
!pip install Augmentor
```


```python
import numpy as np
import os, shutil
from os import rename, listdir
from os.path import isfile, join
import PIL
from PIL import Image
import Augmentor
import tensorflow as tf
from tensorflow.keras import layers
from tensorflow import keras

# load_img 함수: 이미지 불러오기
# img_to_array함수 : 불러온 이미지를 numpy 배열 (ndarray)로 변환
# local에서 사용하려면 Pillow를 설치해야 한다. (pip install Pillow)
from keras.preprocessing.image import ImageDataGenerator, array_to_img, img_to_array, load_img
import matplotlib.pyplot as plt
import numpy as np

# split data
from sklearn.model_selection import train_test_split

# library import
import re
import random
import xml.etree.ElementTree as et

import cv2 
from matplotlib.patches import Rectangle # 바운딩 박스를 그림

 # import the necessary packages
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.layers import AveragePooling2D
from tensorflow.keras.layers import Dropout
from tensorflow.keras.layers import Flatten
from tensorflow.keras.layers import Dense
from tensorflow.keras.layers import Input
from tensorflow.keras.models import Model
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras.preprocessing.image import load_img
from tensorflow.keras.utils import to_categorical
from sklearn.preprocessing import LabelBinarizer
from sklearn.metrics import classification_report
from imutils import paths
import matplotlib.pyplot as plt
import argparse

# EfficientNetB0
from tensorflow.keras.applications import EfficientNetB0

# print(tf.__version__)
# print(keras.__version__)
np.random.seed(1)
tf.random.set_seed(1)
```


```python
!pwd
```


```python
# 디렉토리 경로 설정
%cd /content/gdrive/My\ Drive/final_project
```

# Image Augmentation


```python
PATH = "./data/"
img_file_list = os.listdir(PATH)

# 확장자가 .png인 파일명 조회, 파일 확장자 분리 .splitext
img_list = [fname for fname in picture_file_list if os.path.splitext(fname)[-1]=='.png']
```


```python
# 데이터 증강 방법 중 하나
# img = Augmentor.Pipeline(PATH)

# # 상하 반전
# img.flip_top_bottom(probability=1.0) # 해당 데이터만 가능 다른 데이터는 불가능하다.
# img.sample(10)
```


```python
# 데이터 증강 <- 그냥 여러번 진행했습니다.
# 직선의 경우 기울기를 많이 돌려야 하지 않아야 해서 1로 설정
data_datagen = ImageDataGenerator(rescale=1./255,
                                   rotation_range=1, # 지정된 각도 범위 내에서 임의로 원본 이미지 회전
                                #    shear_range=0.5,  
                                   width_shift_range=0.1,
                                   height_shift_range=0.1,
                                #    horizontal_flip=True,
                                #    vertical_flip=True,
                                   fill_mode='nearest') 
 
filename_in_dir = [] 
 
for root, dirs, files in os.walk('./data'):
    for  fname in files:
        full_fname = os.path.join(root, fname)
        filename_in_dir.append(full_fname)
 
for file_image in img_file_list:
    print(file_image)
    img = load_img(file_image) 
    x = img_to_array(img)
    x = x.reshape((1,) + x.shape)
 
    i = 0
 
    for batch in data_datagen.flow(x,save_to_dir='./data/output', save_prefix='changed', save_format='png'):
        i += 1
        if i > 6:
            break
```

# Image Preprocessing<br>
이미지의 크기와 형태를 확인해보자


```python
# img_list
img = cv2.imread('./data/00001.png', cv2.IMREAD_UNCHANGED)
# File Size : 579Kb
print("Image Size : ",img.size) # (475 x 600 x 3) ==> 855Kb
print("Image Shape : ",img.shape) # (height, width, channel)
print("Image Data Type : ", img.dtype) # unsigned integer 8 bit
# cv2.imwrite("00001.jpg", img) # file size : 173 Kb jpg로 바꾸면 크기 바뀐다던데 전혀 안바뀌더라구요..^^..
```

이미지 전처리를 하기 전에 이미지를 확인해봅시다


```python
import imutils # opencv의 부족한 점을 채워준다 머시기..
from google.colab.patches import cv2_imshow # colab에서 쓸 수 있는 imshow
image = "./train/changed_0_9039.png"
result_path = "./new_train/changed_0_9039.png"
image = cv2.imread(image)
image = cv2.resize(image, dsize=(224,224), interpolation = cv2.INTER_LINEAR)
cv2.imwrite(result_path, image)
cv2_imshow(image)
cv2.waitKey(0)
```

각각 train, test를 resize


```python
# 이미지 resize (224,224)
result_path = './new_train/'
for img in os.listdir('./train'):
    src = cv2.imread("./train/" + img)
    dst = cv2.resize(src, dsize=(224,224), interpolation = cv2.INTER_LINEAR)
    cv2.imwrite(result_path+img,dst)
```


```python
# 이미지 resize (224,224, 3)
result_path = './new_test/'
for img in os.listdir('./test'):
    src = cv2.imread("./test/" + img)
    dst = cv2.resize(src, dsize=(224,224), interpolation = cv2.INTER_LINEAR)
    cv2.imwrite('./new_test/'+img,dst)
```

# MobileNetV2 Fine Tuning


```python
# 파일명을 바꾸려고 했는 데, 파일 수만 줄어들고 이름은 안 바껴서 포기!
# i = 1
# for name in img_file_list:
#     print(name)
#     src = os.path.join(os.getcwd()+'/data/output', name)
#     dst = str(i).zfill(4) + '.png'
#     dst = os.path.join(os.getcwd()+'/data/output', dst)
#     os.rename(src, dst)
#     i+1
```

데이터를 train, test셋으로 옮겨주려고 합니다. 이 때, 파일은 이미 생성되어 있어야 합니다.


```python
# https://code.tutsplus.com/ko/tutorials/file-and-directory-operations-using-python--cms-25817
# shutil.copy(원본경로, 복사할 경로)
import shutil

def copy_to_train(img_list, train_path, test_path):
    count = 0
    current_label = None
    train_len = int(len(img_list)*0.7) # 70%를 train으로 넣어줌
    random.shuffle(img_list)

    for img_name in img_list:
        if count < train_len:
            shutil.copy(PATH + '/' + img_name, train_path) # 이미지 copy
        else:
            shutil.copy(PATH + '/' + img_name, test_path)

        count += 1
```

이진 분류가 아닌 1개를 학습시키므로


```python
copy_to_train(img_list,"./train",'./test')
```


```python
# ImageDataGenerator는 데이터 증강, resize에 사용했다
# https://tykimos.tistory.com/13
# https://keras.io/ko/preprocessing/image/
def get_generators():
    '''
    train, validation, test generator를 생성해서 반환.
    train generator는 image 변환 처리
    '''
    train_dir = './train2'
    validation_dir = './test2'
    
    train_datagen = ImageDataGenerator(rescale=1/255,
                                       rotation_range=40,
                                       brightness_range=(0.7,1.3),
                                    #    zoom_range=0.2,
                                       horizontal_flip=True)
    
    test_datagen = ImageDataGenerator(rescale=1/255) #validation/test에서 사용

    # generator 들 생성
    train_generator = train_datagen.flow_from_directory(train_dir,
                                                        target_size=(224,224),
                                                        batch_size=N_BATCHS)
                                                        # class_mode='binary')
    val_generator = test_datagen.flow_from_directory(validation_dir,
                                                    target_size=(224,224),
                                                    batch_size=N_BATCHS)
                                                    # class_mode='binary')
    return train_generator, val_generator
```


```python
conv_base = MobileNetV2(weights="imagenet", include_top=False,input_tensor=Input(shape=(224,224,3)))
```


```python
LEARNING_RATE = 0.002
N_EPOCHS = 20
N_BATCHS = 100
IMAGE_SIZE = 224
N_CLASS = 1
DROPOUT_RATE = 0.3
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
    # model.add(layers.BatchNormalization())
    model.add(layers.Dense(128, activation='relu'))

    # 출력
    # 출력 레이어를 2개 이상으로 두어 함수형 모델로도 사용가능하다.
    model.add(layers.Dense(1, activation='sigmoid'))

    return model
```


```python
model = create_model()
model.compile(optimizer=keras.optimizers.Adam(learning_rate=LEARNING_RATE),
              loss='mean_squared_error', metrics=['accuracy']) # loss='binary_crossentropy'
model.summary()
```


```python
train_iterator, validation_iterator = get_generators()
```

모델 fit


```python
# h_callback = keras.callbacks.ModelCheckpoint('./models', monitor='val_loss', save_best_only=True)

history = model.fit(train_iterator,
                    epochs=N_EPOCHS,
                    steps_per_epoch=len(train_iterator),
                    validation_data=validation_iterator,
                    validation_steps=len(validation_iterator))
```

모델 저장


```python
model.save("my_model")
model.save("my_h5_model.h5")
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
# plt.savefig(args["plot"])
```
