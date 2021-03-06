# 사이킷런
# LSTM 으로 모델링
# Dense와 성능비교
# 회귀

import numpy as np

from sklearn.datasets import load_boston

#1. 데이터
dataset = load_boston()
x = dataset.data
y = dataset.target
print(x.shape)  # (506, 13)
print(y.shape)  # (506,)
print("==========================")
print(x[:5])
print(y[:10])

print(np.max(x), np.min(x))
print(dataset.feature_names)
print(dataset.DESCR)

from sklearn.model_selection import train_test_split
x_train, x_test, y_train, y_test = train_test_split(
        x, y, train_size=0.8, random_state=66, shuffle=True
)

from sklearn.preprocessing import MinMaxScaler
scaler = MinMaxScaler()
scaler.fit(x)
x_train = scaler.transform(x_train)
x_test = scaler.transform(x_test)

print(x.shape)          # (506, 13)
print(x_train.shape)    # (404, 13)
print(x_test.shape)     # (102, 13)

x = x.reshape(x.shape[0], x.shape[1], 1)
x_train = x_train.reshape(x_train.shape[0], x_train.shape[1], 1)
x_test = x_test.reshape(x_test.shape[0], x_test.shape[1], 1)

#2. 모델 구성
from tensorflow.keras.models import Sequential, Model
from tensorflow.keras.layers import Dense, Input, LSTM
model = Sequential()
model.add(LSTM(10, activation='relu', input_shape=(13,1)))
model.add(Dense(26, activation='relu'))      
model.add(Dense(65, activation='relu'))      
model.add(Dense(13, activation='relu'))      
model.add(Dense(13, activation='relu')) 
model.add(Dense(1))

model.summary()

#3. 컴파일, 훈련
model.compile(loss='mse', optimizer='adam')

from tensorflow.keras.callbacks import EarlyStopping
es = EarlyStopping(monitor='loss', patience=30, mode='auto')
model.fit(x_train, y_train, epochs=300, batch_size=13,
          validation_split=0.2, verbose=1)

#4. 평가, 예측
loss = model.evaluate(x_test, y_test, batch_size=1)
print("loss: ", loss)

y_predict = model.predict(x_test)
# print(y_predict)

# RMSE 구하기
from sklearn.metrics import mean_squared_error
def RMSE(y_test, y_predict):
    return np.sqrt(mean_squared_error(y_test, y_predict))
print("RMSE : ", RMSE(y_test, y_predict))
print("mse : ", mean_squared_error(y_predict, y_test))

# R2
from sklearn.metrics import r2_score
r2 = r2_score(y_test, y_predict)
print("R2 : ", r2)

# sklearn Dense boston
# loss, mae :  15.000182151794434 2.9936561584472656
# RMSE :  3.873007354200969
# mse :  15.00018596569479
# R2 :  0.8205353096631526

# sklearn LSTM boston
# loss:  13.589542388916016
# RMSE :  3.6863995903399993
# mse :  13.589541939658915
# R2 :  0.8374124866452932