# 실습 : 코드를 완성할 것
# mlp4처럼 predict값을 도출할것
# 1:다 mlp

import numpy as np
#1. 데이터
x = np.array([range(100)])
y = np.array([range(711, 811), range(1,101), range(201, 301)])
print(x.shape)      # (1, 100)
print(y.shape)      # (3, 100)
x_pred2 = np.array([401])
print("x_pred2.shape : ", x_pred2.shape)     # (1, )     

# x = np.arange(20).reshape(10,2)
x = np.transpose(x)
y = np.transpose(y)
x_pred2 = x_pred2.reshape(1, 1)

print(x)
print(x.shape)      # (100, 1)
print(y.shape)      # (3, 100)
print("x_pred2.shape : ", x_pred2.shape)    #(1, 1) 

from sklearn.model_selection import train_test_split
x_train, x_test, y_train, y_test = train_test_split(
        x, y, train_size=0.8, random_state=66, shuffle=True
)
print(x_train.shape)        # (80, 1)
print(y_train.shape)        # (80, 3)

#2. 모델 구성
from tensorflow.keras.models import Sequential, Model
from tensorflow.keras.layers import Dense, Input
# from keras.layers import Dense

input1 = Input(shape=(1,))
dense1 = Dense(5, activation='relu')(input1)
dense2 = Dense(3)(dense1)
dense3 = Dense(4)(dense2)
outputs = Dense(3)(dense3)
model = Model(inputs = input1, outputs = outputs)
model.summary()

# model = Sequential()
# model.add(Dense(10, input_dim=1))
# model.add(Dense(5))
# model.add(Dense(5))
# model.add(Dense(3))


#3. 컴파일, 훈련
model.compile(loss='mse', optimizer='adam', metrics=['mae'])
model.fit(x_train, y_train, epochs=100, batch_size=1, 
          validation_split=0.2)

#4. 평가, 예측
loss, mae = model.evaluate(x_test, y_test)
print('loss : ', loss)
print('mae : ', mae)

y_predict = model.predict(x_test)
# print(y_predict)

# RMSE
from sklearn.metrics import mean_squared_error
def RMSE(y_test, y_predict):
    return np.sqrt(mean_squared_error(y_test, y_predict))
print("RMSE : ", RMSE(y_test, y_predict))
# print("mse : ", mean_squared_error(y_test, y_predict))
print("mse : ", mean_squared_error(y_predict, y_test))

# R2
from sklearn.metrics import r2_score
r2 = r2_score(y_test, y_predict)
print("R2 : ", r2)

y_pred2 = model.predict(x_pred2)
print(y_pred2)
