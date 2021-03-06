# 실습 : 19_1, 2, 3, 4, 5, EarlyStopping까지
# 총 6개의 파일을 완성하시오.

# 1. 데이터
import numpy as np
from sklearn.datasets import load_diabetes

datasets = load_diabetes()
x = datasets.data
y = datasets.target

print(x.shape, y.shape) # (442, 10) (442,)
print(x[:5])
print(y[:10])
 

print(np.max(x), np.min(x)) # 0.198787989657293 -0.137767225690012
print(datasets.feature_names)
print(datasets.DESCR)

from sklearn.model_selection import train_test_split
x_train, x_test, y_train, y_test = train_test_split(
        x, y, train_size=0.8, random_state=66, shuffle=True
)

# 2. 모델 구성
from tensorflow.keras.models import Sequential, Model
from tensorflow.keras.layers import Dense, Input

input1 = Input(shape=(10,))
dense1 = Dense(100, activation='relu')(input1)
dense1 = Dense(200, activation='relu')(input1)
dense1 = Dense(500, activation='relu')(input1)
dense1 = Dense(500, activation='relu')(input1)
dense1 = Dense(500, activation='relu')(input1)
dense1 = Dense(500, activation='relu')(input1)
dense1 = Dense(500, activation='relu')(input1)
outputs = Dense(1)(dense1)
model = Model(inputs = input1, outputs = outputs)
model.summary

# 3. 컴파일, 훈련
model.compile(loss='mse', optimizer='adam', metrics=['mae'])

from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint
es = EarlyStopping(monitor='loss', patience=30, mode='auto')
modelpath = '../data/modelcheckpoint/k46_MC_5_diabets_{epoch:02d}-{val_loss:.4f}.hdf5'
cp = ModelCheckpoint(filepath=modelpath, monitor='val_loss', save_best_only=True, mode='auto')
hist = model.fit(x_train, y_train, batch_size=8, epochs=100, validation_split=0.2, 
                 verbose=1, callbacks=[es, cp])

# 4. 평가 예측
result = model.evaluate(x_test, y_test, batch_size=8)
print("loss, mae : ", result[0], result[1])

y_predict = model.predict(x_test)
# print(y_predict)

# RMSE 구하기
from sklearn.metrics import mean_squared_error
def RMSE(y_test, y_predict):
    return np.sqrt(mean_squared_error(y_test, y_predict))
print("RMSE : ", RMSE(y_test, y_predict))
print("mse : ", mean_squared_error(y_test, y_predict))

# R2
from sklearn.metrics import r2_score
r2 = r2_score(y_test, y_predict)
print("R2 : ", r2)

# 시각화
import matplotlib.pyplot as plt

plt.figure(figsize=(10, 6)) # 단위 알아서 찾을 것!

plt.subplot(2, 1, 1)    # 2행 1열중 첫번째
plt.plot(hist.history['loss'], marker='.', c='red', label='loss')
plt.plot(hist.history['val_loss'], marker='.', c='blue', label='val_loss')
plt.grid()

# plt.title('Cost loss')    # 한글깨짐 오류 해결할 것 과제1.
plt.ylabel('loss')
plt.xlabel('epoch')
plt.legend(loc='upper right')

plt.subplot(2, 1, 2)    # 2행 2열중 두번째
plt.plot(hist.history['mae'], marker='.', c='red', label='mae')
plt.plot(hist.history['val_mae'], marker='.', c='blue', label='val_mae')
plt.grid()

# plt.title('정확도')
plt.ylabel('mae')
plt.xlabel('epoch')
plt.legend(loc='upper right')

plt.show()

# keras Dense diabets
# loss, mae :  3393.61083984375 47.12013244628906
# RMSE :  58.2547106883262
# mse :  3393.611317380587
# R2 :  0.47710474684639814

# keras MC_5_diabets
# loss, mae :  3361.239013671875 47.84621810913086
# RMSE :  57.976194756945915
# mse :  3361.239158495323
# R2 :  0.48209272178882745




