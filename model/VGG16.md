```python
import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.applications import VGG16, ResNet50V2, mobilenet_v2
from tensorflow.keras.preprocessing.image import ImageDataGenerator

# 하이퍼 파라미터
LEARNING_RATE = 0.001
N_EPOCHS = 20
N_BATCHS = 20
NUM_CLASSES = 10 # 클래스 개수
INPUT_SHAPE = (640, 480, 3) # 학습할 이미지 shape
FEATURE_SHAPE = (20, 15, 512)

# 학습데이터 및 모델 경로 설정
train_dir = './data/train'
validation_dir = './data/validation'
test_dir = './data/test'
MODEL_PATH = './models/cat_dog_model'


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
                                                        class_mode='binary')    
    val_generator = test_datagen.flow_from_directory(validation_dir,
                                                        target_size=INPUT_SHAPE[:2],
                                                        batch_size=N_BATCHS,
                                                        class_mode='binary')
    test_generator = test_datagen.flow_from_directory(test_dir,
                                                        target_size=INPUT_SHAPE[:2],
                                                        batch_size=N_BATCHS,
                                                        class_mode='binary')
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
  return_labels = np.zeros(shape=(sample_counts,)) # label 저장

  datagen = ImageDataGenerator(rescale=1./255)
  iterator = datagen.flow_from_directory(image_directory,
                                         target_size=INPUT_SHAPE[:2],
                                         batch_size=N_BATCHS,
                                         class_mode='binary')
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
  model.add(layers.Dense(256, activation='relu'))
  model.add(layers.Dense(1, activation='sigmoid'))

  return model
```



```python
# Featuremap 추출
train_features, train_labels = extract_featuremap(train_dir, 2000)
validation_features, validation_labels = extract_featuremap(validation_dir, 1000)
test_features, test_labels = extract_featuremap(test_dir, 1000)

mc_callback = keras.callbacks.ModelCheckpoint(MODEL_PATH), monitor='val_loss', save_best_only=True)

train_iterator, validation_iterator, test_iterator = get_generators()

model = create_model()
model.compile(optimizer=keras.optimizers.Adam(learning_rate=LEARNING_RATE), 
              loss='binary_crossentropy', # 클래스 따라 변경
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

# evaluation
best_model.evaluate(train_iterator)
best_model.evaluate(test_iterator)
```
