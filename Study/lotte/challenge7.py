import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow import keras
from keras.preprocessing.image import ImageDataGenerator
from keras import Sequential
from keras.layers import *
from keras.callbacks import EarlyStopping, ModelCheckpoint, ReduceLROnPlateau
from keras.optimizers import Adam
from sklearn.model_selection import train_test_split
from tensorflow.keras.applications import VGG16, VGG19, Xception
from tensorflow.keras.applications import ResNet101, ResNet101V2, ResNet152, ResNet152V2
from tensorflow.keras.applications import ResNet50, ResNet50V2
from tensorflow.keras.applications import InceptionV3, InceptionResNetV2
from tensorflow.keras.applications import MobileNet, MobileNetV2
from tensorflow.keras.applications import DenseNet121, DenseNet169, DenseNet201
from tensorflow.keras.applications import NASNetLarge, NASNetMobile
from tensorflow.keras.applications import EfficientNetB3, EfficientNetB4, EfficientNetB5, EfficientNetB6, EfficientNetB7
from tensorflow.keras.applications.efficientnet import preprocess_input
from sklearn.model_selection import train_test_split
from sklearn.model_selection import KFold
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint, ReduceLROnPlateau

# 데이터 지정 및 전처리
x = np.load("../study/LPD_COMPETITION/npy/P_project_x4.npy", allow_pickle=True)
y = np.load("../study/LPD_COMPETITION/npy/P_project_y4.npy", allow_pickle=True)
x_pred = np.load('../study/LPD_COMPETITION/npy/pred.npy', allow_pickle=True)

print(x.shape, y.shape, x_pred.shape)   # (48000, 64, 64, 3) (48000, 1000) (72000, 64, 64, 3)

idg = ImageDataGenerator(
    width_shift_range=(-1,1),   
    height_shift_range=(-1,1),  
    shear_range=0.2)    # 현상유지

idg2 = ImageDataGenerator()

# y = np.argmax(y, axis=1)

x = preprocess_input(x) 
x_pred = preprocess_input(x_pred) 

x_train, x_valid, y_train, y_valid = train_test_split(x, y, train_size = 0.8, shuffle = True, random_state=42)

train_generator = idg.flow(x_train, y_train, batch_size=64, seed=48)
# seed => random_state
valid_generator = idg2.flow(x_valid, y_valid)
test_generator = x_pred

kfold = KFold(n_splits=5, shuffle=True)

from tensorflow.keras import regularizers
from tensorflow.keras.models import Model, Sequential, load_model
from tensorflow.keras.layers import GlobalAveragePooling2D, Flatten, BatchNormalization, Dense, Activation, Dropout, Conv2D
# EfficientNetB4 = EfficientNetB4(include_top=False, weights='imagenet', input_shape=x_train.shape[1:])
# EfficientNetB4.trainable = True
# model = Sequential()
# model.add(EfficientNetB4)
# model.add(Conv2D(128, 1, padding='same', activation='swish', 
#            kernel_regularizer=regularizers.l2(1e-5),        # 1e-5 
#            activity_regularizer=regularizers.l1(1e-5)))     # 1e-5
# model.add(GlobalAveragePooling2D())
# model.add(GaussianDropout(0.5))                      
# model.add(Flatten())
# model.add(Dense(1000, activation= 'softmax'))

# # MobileNet.summary()
# model.summary()

mc = ModelCheckpoint('../study/LPD_COMPETITION/h5/challenge22.hdf5', save_only_true=True, verbose=1)
es = EarlyStopping(patience=30)
reduce_lr = ReduceLROnPlateau(patience=15, factor=0.5)

for train_index, test_index in kfold.split(x):

    x_train, x_test = x[train_index], x[test_index]
    y_train, y_test = y[train_index], y[test_index]

    x_train, x_valid, y_train, y_valid = train_test_split(x, y, train_size = 0.8, shuffle = True, random_state=42)

    EfficientNetB4 = EfficientNetB4(include_top=False, weights='imagenet', input_shape=x_train.shape[1:])
    EfficientNetB4.trainable = True
    model = Sequential()
    model.add(EfficientNetB4)
    model.add(Conv2D(128, 1, padding='same', activation='swish', 
            kernel_regularizer=regularizers.l2(1e-5),        # 1e-5 
            activity_regularizer=regularizers.l1(1e-5)))     # 1e-5
    model.add(GlobalAveragePooling2D())
    model.add(GaussianDropout(0.5))                      
    model.add(Flatten())
    model.add(Dense(1000, activation= 'softmax'))

    # MobileNet.summary()
    model.summary()

    model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['acc'],
                  callbacks=[es, reduce_lr, mc], steps_per_epoch= len(x_train) / 64)

    # model.load_weights('../study/LPD_COMPETITION/h5/challenge23.hdf5')
    # model = load_model('../study/LPD_COMPETITION/h5/challenge23.hdf5')

# predict
result = model.predict(test_generator,verbose=True)
   
print(result.shape)
sub = pd.read_csv('../study/LPD_COMPETITION/sample.csv')
sub['prediction'] = np.argmax(result, axis = 1)
sub.to_csv('../study/LPD_COMPETITION/answer/answer23.csv', index=False)