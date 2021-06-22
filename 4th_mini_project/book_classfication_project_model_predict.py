# -*- coding: utf-8 -*-
"""book_classfication_project_model_predict.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1sT59wY869HnRgV8z7zivgZLIhtJC8mqh

## 학습시킨 모델로 알라딘사이트에서 테스트 페이지를 추출해 카테고리를 예측하기
"""

! pip install konlpy

import pandas as pd
import numpy as np
from tensorflow.keras.models import *
import pickle
from konlpy.tag import Okt
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.preprocessing.sequence import pad_sequences

pd.set_option('display.unicode.east_asian_width', True)  #줄맞춤

#토큰 불러오기

with open('nouns_token.pickle', 'rb') as f:
    token = pickle.load(f)

#라벨인코더 불러오기

with open('/content/nouns_category_onehot_encoder.pickle', 'rb') as f:
    encoder = pickle.load(f)

category = encoder.categories_[0]
print(category)

#카테고리별로 페이지를 지정해(p.444~446) 크롤링한 책 제목과 내용 불러오기
df = pd.read_csv('/content/raw_test_2021-06-22.csv')

print(df.head())

print(df.info())

# 결측값 제거
df.reset_index(inplace=True)
df.drop_duplicates(subset=['title'], inplace=True)
df.dropna(inplace=True)
df.reset_index(drop=True, inplace=True)
print(df['title'].duplicated().sum())

#데이터를 피쳐와 타켓으로 분류

X = df['title'] + " " + df['summary']
Y = df['category']

# for문을 사용해서 X전체 텍스트를 형태소 단위로 분리시키기
okt = Okt()
for i in range(len(X)):
    X[i] = okt.nouns(X[i])
print(X)

# 형태소로 잘라 낸 뒤, 의미 없는 조사, 접속사, 감탄사 같은 단어들은 제거하기 위해 이 단어들을 모아놓은 파일 가져오기

stopwords = pd.read_csv('stopwords.csv')

# 한 글자인 단어와, stopwords로 불필요한 단어 제거하기
# 함수로 만들어 기존 데이터에 apply해 stopword 제거
def delete_stopwords(lst):
    words = []
    for word in lst:
        if word not in list(stopwords['stopword']) and len(word) > 1:
            words.append(word)
    return ' '.join(words)

X = X.apply(delete_stopwords)

#토크나이징 작업하기(숫자로 라벨화 작업)

tokened_X = token.texts_to_sequences(X)  #texts_to_sequences = 단어를 시퀀스형태로 변환하기(문장변화는 여기서 일어난다)
print(tokened_X[0])  #첫줄만 확인하기

#612개의 길이를 맞추기 위해 짧은 문장은 앞쪽에 0으로 채워준다

X_pad = pad_sequences(tokened_X, 612)  #pad_sequences= 612이 안되는 문장을 0으로 채워준다(앞쪽에)
print(X_pad[:10])

#모델 불러오기

model = load_model('/content/drive/MyDrive/projects/book_classfication_0.9078609347343445.h5')

#모델을 이용해 예측하기

predict = model.predict(X_pad)
print(predict[0])  #첫줄을 예측

# predict에서 가장 값이 큰 인덱스만 가져오기

predict_category = []
for pred in predict:
    predict_category.append(category[np.argmax(pred)])

print(predict_category)

#컬럼 추가
df['predict'] = predict_category
print(df.head())

#OX컬럼에 타이틀과 predict이 맞으면 o 아니면 x로 표기
df['OX'] = df.apply(lambda x: 'O' if x['predict']==x['category'] else 'X', axis=1)

#예측률 확인하기

print(df['OX'].value_counts() / len(df['OX']))

df.tail()

#내용 확인해보기

df.iloc[-30:, 0:5]