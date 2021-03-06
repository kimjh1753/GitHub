# CNN 으로 구성
# 2차원을 4차원으로 늘여서 하시오.

import numpy as np
from sklearn.datasets import load_wine

dataset = load_wine()
print(dataset.DESCR)
print(dataset.feature_names)

# ['alcohol', 'malic_acid', 'ash', 'alcalinity_of_ash', \
# 'magnesium', 'total_phenols', 'flavanoids', 'nonflavanoid_phenols', \
# 'proanthocyanins', 'color_intensity', 'hue', 'od280/od315_of_diluted_wines', 'proline']

# 1. 데이터

x = dataset.data
y = dataset.target

print(x)        # preprocessing 해야 함
print(y)        # 0, 1, 2 >> 다중분류
print(x.shape)  # (178, 13)
print(y.shape)  # (178,)

from sklearn.model_selection import train_test_split
x_train, x_test, y_train, y_test = train_test_split(
        x, y, train_size = 0.8, random_state = 66, shuffle = True
)

from sklearn.preprocessing import MinMaxScaler
scaler = MinMaxScaler()
scaler.fit(x)
x = scaler.transform(x)
x_train = scaler.transform(x_train)
x_test = scaler.transform(x_test)

print(x.shape)          # (178, 13) 
print(x_train.shape)    # (142, 13)
print(x_test.shape)     # (36, 13) 

print(x_train.shape[0], x_train.shape[1])

x_train = x_train.reshape(x_train.shape[0], x_train.shape[1], 1, 1)
x_test = x_test.reshape(x_test.shape[0], x_test.shape[1], 1, 1)

print(x_train.shape, x_test.shape)  # (142, 13, 1, 1) (36, 13, 1, 1)

from tensorflow.keras.utils import to_categorical
y = to_categorical(y)
y_train = to_categorical(y_train)
y_test = to_categorical(y_test)

print(y.shape)          # (178, 3)
print(y_train.shape)    # (142, 3)

# 2. 모델 구성
from tensorflow.keras.models import Sequential, Model
from tensorflow.keras.layers import Dense, LSTM, Conv2D, Flatten, Dropout

model = Sequential()
model.add(Conv2D(filters=10, kernel_size=(2,2), padding='same',
          strides=1, input_shape=(13, 1, 1)))
model.add(Dropout(0.2))
model.add(Conv2D(10, (2,2), padding='same'))
model.add(Flatten())
model.add(Dense(1000, activation='relu'))
model.add(Dropout(0.2))
model.add(Dense(1000, activation='relu'))
model.add(Dropout(0.2))
model.add(Dense(1000, activation='relu'))
model.add(Dropout(0.2))
model.add(Dense(1000, activation='relu'))
model.add(Dropout(0.2))
model.add(Dense(1000, activation='relu'))
model.add(Dropout(0.2))
model.add(Dense(3, activation='softmax'))

model.summary()

# 3. 컴파일, 훈련
model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['acc'])

from tensorflow.keras.callbacks import EarlyStopping
early_stopping = EarlyStopping(monitor='loss', patience=30, mode='auto')

model.fit(x_train, y_train, epochs=3000, validation_split=0.2, 
          verbose=1, batch_size=13, callbacks=[early_stopping])

# 4. 평가, 예측
loss, accuracy = model.evaluate(x_test, y_test, batch_size=1)
print("loss : ", loss)
print("accruacy : ", accuracy)

# sklearn Dense wine
# loss :  0.6666666865348816
# accruacy :  0.3333333432674408

# sklearn LSTM wine
# loss :  0.022735370323061943
# accruacy :  0.9722222089767456

# sklearn cnn wine
# loss :  0.09509149193763733
# accruacy :  0.9722222089767456