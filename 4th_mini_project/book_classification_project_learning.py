# -*- coding: utf-8 -*-
"""book_classfication_project_learning.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1LZL4e3UyAZghPke0DsSsehnoF8S8wCHE

## 전처리 데이터를 모델로 학습시키기
"""

#모듈 불러오기
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import *

#전처리 된 데이터 불러오기

X_train, X_test, Y_train, Y_test = np.load('/content/drive/MyDrive/projects/nouns_books_data_max_612_size_68561.npy', allow_pickle=True)

print(X_train.shape)
print(X_test.shape)
print(Y_train.shape)
print(Y_test.shape)

# 모델 생성하기

model = Sequential()
#Embedding=라벨링 된 데이터를 원 핫 인코딩 해서 벡터라이징역할(단어들간의 수치적인 관계를 형성시켜준다=단어가 같은 의미들이 같은 방향에 있게끔)
#뒤에는 단어의 총 개수를 주어야한다(=차원의 수)
#output_dim=300,  # 차원 축소 / 차원이 너무 커지면 데이터가 희소해지기 때문에 차원을 300차원으로 제한 (적은 차원에 데이터들을 압축해서 넣음)
model.add(Embedding(68561, 300, input_length=612))  #input_length= 문장의 길이를 줘야한다
model.add(Conv1D(64, kernel_size=5, padding='same', activation='relu'))
model.add(MaxPool1D(pool_size=1))
model.add(LSTM(128, activation='tanh'))  #순서가 있는 문장이기에 LSTM을 사용해준다, return_sequences=True면 앞에 학습이 모두 출력되고, false면 맨 끝 하나만 출력
model.add(Dropout(0.6))
model.add(Flatten())
model.add(Dense(256, activation='relu'))
model.add(Dropout(0.6))
model.add(Dense(8, activation='softmax'))  #카테고리=8개라서 8

print(model.summary())

# 모델 학습 설정

model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
fit_hist = model.fit(X_train, Y_train, batch_size=300, epochs=5, validation_data=(X_test, Y_test))

score = model.evaluate(X_test, Y_test)
print(score[1])  #정확도

# 모델 저장하기

model.save('news_classfication_{}.h5'.format(score[1]))