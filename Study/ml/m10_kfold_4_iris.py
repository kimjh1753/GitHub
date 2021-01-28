# 실습
# 6개의 모델을 완성하라!
# for문 쓸 수 있는 사람은 써봐라!! 후훗

import numpy as np
from sklearn.datasets import load_iris
from sklearn.preprocessing import MinMaxScaler, StandardScaler
from sklearn.model_selection import train_test_split, KFold, cross_val_score
from sklearn.metrics import accuracy_score

from sklearn.svm import LinearSVC, SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier

import warnings
warnings.filterwarnings('ignore')

# 1. 데이터
# x, y = load_iris(return_X_y=True)

dataset = load_iris()
x = dataset.data
y = dataset.target
# print(dataset.DESCR)
# print(dataset.feature_names)

print(x.shape, y.shape)      # (150, 4) (150, )

x_train, x_test, y_train, y_test = train_test_split(
    x, y, random_state=77, shuffle=True, train_size=0.8
)

kfold = KFold(n_splits=5, shuffle=True)

# 2. 모델 구성
# model = LinearSVC()
# model = SVC()
# model = KNeighborsClassifier()
# model = LogisticRegression()
# model = DecisionTreeClassifier()
model = RandomForestClassifier()

scores = cross_val_score(model, x_train, y_train, cv=kfold)
print('scores : ', scores)

# model = [LinearSVC(), SVC(), KNeighborsClassifier(), LogisticRegression(), DecisionTreeClassifier(), RandomForestClassifier()]
# for i in range(6):
#     scores = cross_val_score(model[i], x_train, y_train, cv=kfold)
#     print('scores : ', scores)

'''
# model = LinearSVC()
# scores :  [1.         1.         0.83333333 1.         0.93333333]

# model = SVC()
# scores :  [1.         1.         0.95833333 0.91666667 0.91666667]

# model = KNeighborsClassifier()
# scores :  [0.95833333 1.         1.         0.95833333 1.        ]

# model = LogisticRegression()
# scores :  [0.95833333 1.         0.875      1.         0.95833333]

# model = DecisionTreeClassifier()
# scores :  [0.91666667 0.95833333 0.95833333 1.         1.        ]

# model = RandomForestClassifier()
# scores :  [1.         0.95833333 1.         0.95833333 0.95833333]
'''
