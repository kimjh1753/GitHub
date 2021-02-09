import numpy as np
from tensorflow.keras.preprocessing.image import ImageDataGenerator

train_datagen = ImageDataGenerator(
    rescale=1./255,
    horizontal_flip=True,   # 수평방향으로 뒤집기
    vertical_flip=True,     # 수직방향으로 뒤집기
    width_shift_range=0.1,  # 지정된 수평방향 이동 범위내에서 임의로 원본이미지를 이동
    height_shift_range=0.1, # 지정된 수직방향 이동 범위내에서 임의로 원본이미지를 이동
    rotation_range=5,       # 지정된 각도 범위내에서 임의로 원본이미지를 회전
    zoom_range=1.2,         # 지정된 확대/축소 범위내에서 임의로 원본이미지를 확대/축소
    shear_range=0.7,        # 밀림 강도 범위내에서 임의로 원본이미지를 변형
    fill_mode='nearest'     # 빈자리를 채워준다
)
test_datagen = ImageDataGenerator(rescale=1./255) # 원래 값 0 ~ 255 -> rescale 후 0 ~ 1
# 테스트는 왜 리스케일만 할까?
# 시험문제는 건들 필요가 없기 때문이다

# flow 또는 flow_from_directory

# train_generator
xy_train = train_datagen.flow_from_directory(
    '../data/image/brain/train', 
    target_size=(150, 150),
    batch_size=10,                              # 출력되는 y값 개수 설정
    class_mode='binary'
)                                               # (80, 150, 150, 1)
# Found 160 images belonging to 2 classes.

# test_generator
xy_test = test_datagen.flow_from_directory(
    '../data/image/brain/test', 
    target_size=(150, 150),
    batch_size=5,
    class_mode='binary'
)
# Found 120 images belonging to 2 classes.

print(xy_train) 
print(xy_test)  
# <tensorflow.python.keras.preprocessing.image.DirectoryIterator object at 0x00000238EC938550>
print(xy_train[0])
print(xy_train[0][0])        # x값
print(xy_train[0][0].shape)  # (5, 150, 150, 3) 
print(xy_train[0][1])        # [1. 0. 1. 0. 1. 1. 0. 1. 0. 1.]  10개가 있데??? -> y값
print(xy_train[0][1].shape)  # (10,) 
# print(xy_train[15][1].shape) # (10,)          

# 160장을 batch_size 10으로 나눔 160/10 = 16 -> [0] ~ [15]


