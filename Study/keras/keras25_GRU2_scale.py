# 실습
# keras23_LSTM1 로 GRU코드 완성
# GRU 파라미터 분석할 것
# 결과치(loss와 predict값)을 LSTM과 비교

# keras23_LSTM3_scale.py를 카피

import numpy as np
# 1. 데이터
x = np.array([[1,2,3], [2,3,4], [3,4,5], [4,5,6],
              [5,6,7], [6,7,8], [7,8,9], [8,9,10],
              [9,10,11], [10,11,12],
              [20,30,40], [30,40,50], [40,50,60]])
y = np.array([4,5,6,7,8,9,10,11,12,13,50,60,70])
x_pred = np.array([50,60,70])

print("x.shape : ", x.shape)    # (13, 3)
print("y.shape : ", y.shape)    # (13,)
print("x_pred : ", x_pred.shape) # (3,)

# 코딩하시오!!! LSTM
# 나는 80을 원하고 있다.

x_pred = x_pred.reshape(1, 3)

from sklearn.preprocessing import MinMaxScaler
scaler = MinMaxScaler()
scaler.fit(x)
x = scaler.transform(x)
x_pred = scaler.transform(x_pred)

x = x.reshape(13, 3, 1)
x_pred = x_pred.reshape(1, 3, 1)

# 2. 모델 구성
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, LSTM, SimpleRNN, GRU
model = Sequential()
model.add(GRU(10, activation='relu', input_shape=(3,1)))
model.add(Dense(20))
model.add(Dense(10))
model.add(Dense(1))

model.summary()

# 3. 컴파일, 훈련
model.compile(loss='mse', optimizer='adam', metrics=['mae'])

from tensorflow.keras.callbacks import EarlyStopping
early_stopping = EarlyStopping(monitor='loss', patience=20, mode='auto')
model.fit(x, y, epochs=3000, batch_size=1, callbacks=[early_stopping])

# 4. 평가, 예측
loss = model.evaluate(x, y, batch_size=1)
print(loss)

result = model.predict(x_pred)
print(result)

# LSTM
# [0.006796032190322876, 0.07546142488718033]
# [[80.307556]]

# SimpleRNN
# [0.0005277382442727685, 0.017353352159261703]
# [[80.09282]]

# GRU
# [0.3488308787345886, 0.5341994762420654]
# [[80.286316]]
