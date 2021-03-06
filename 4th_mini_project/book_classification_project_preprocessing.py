# -*- coding: utf-8 -*-
"""book_classfication_project_preprocessing.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1v0oq3acunWkTWuXNNRJ4Y-_lCYG0zNB-

알라딘 사이트에서 책 제목과 책 소개를 크롤링한 데이터 전처리하기
"""

! pip install konlpy

#모듈 불러오기

import pandas as pd
import numpy as np
from tensorflow.keras.utils import to_categorical
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from tensorflow.keras.preprocessing.text import *
from tensorflow.keras.preprocessing.sequence import pad_sequences
import pickle
from konlpy.tag import Okt

#행열 정렬

pd.set_option('display.unicode.east_asian_width',True)

#크롤링한 파일 가져오기

df = pd.read_csv('/content/drive/MyDrive/projects/raw_65548_2021-06-18.csv', engine='python')
print(df.head())

print(df.info())

from google.colab import drive
drive.mount('/content/drive')

#결측값 삭제하기

df= df.dropna(axis=0)

print(df.head())
print(df.info())

#책 이름과 소개에 중복된 내용이 있는지 확인하기

col_dup = df['summary'].duplicated()  #duplicated=중복이라면 true
print(col_dup)
col_dup2 = df['title'].duplicated()
print(col_dup2)
sum_dup = df.summary.duplicated().sum()  #중복 개수 확인
print(sum_dup)

df = df.drop_duplicates(subset=['summary'])  #타이틀과 내용이 중복이라면 중복된 row 제거
df = df.drop_duplicates(subset=['title'])  
sum_dup = df.summary.duplicated().sum()  #제거 후 다시 중복 개수 확인
print(sum_dup) #중복된 개수의 합

#중복이 제거되면 데이터프레임 인덱스가 빠지게 되어 다시 정렬

df.reset_index(drop=True, inplace=True ) #drop=True를 해야 기존 인덱스를 없애줌

#데이터를 나눠준다(피쳐, 타켓값으로)

X = df['title'] + " " + df['summary']  #형태소 분리를 위한 Okt 사용시에, 문자열로 줘야해서 한 컬럼으로 합친다
Y= df['category']

len(X)  #중복을 제거한 피쳐의 개수

print(X[1250:1350])

"""Y값 전처리"""

#Y(타겟)는 문자열로 들어가있기에 라벨로 바꿔준다

encoder = LabelEncoder()
labeled_Y = encoder.fit_transform(Y)  #데이터를 라벨로 바꿔준다 (문자열 8가지를 같은 문자끼리 라벨로 묶어준다)
label = encoder.classes_   #인코더에 등록된 클래스 조회
print(label)    #카테고리 이름확인

#카테고리에서 라벨 순서를 기억해야 해서 따로 저장해 준다

with open('/content/datasets/book_category_encoder.pickle', 'wb') as f:
  pickle.dump(encoder, f)

print(labeled_Y)  #라벨화 시킨 카테고리가 잘변환됐는지 확인

#라벨이 붙은 걸 원핫인코딩으로 변환  (학습시에는 필요하지만, 검증시에는 필요하지 않다)

onehot_Y = to_categorical(labeled_Y)  #희소행렬화
print(onehot_Y)

"""X값 전처리"""

#불용어가 있는 csv파일 불러오기

stopwords= pd.read_csv('/content/datasets/stopwords.csv')

#자연어인 X를 전처리해준다(한글 형태소 분류기 사용 - Okt)

okt = Okt()
print(type(X))
okt_X = okt.morphs(X[0]) # 첫번째 title만 형태소 분리를 해서 okt_X에 넣어줌
print(X[0])
print(okt_X)

# for문을 사용해서 X전체 텍스트를 형태소 단위로 분리시키기 

for i in range(len(X)):
  X[i] = okt.morphs(X[i])
print(X)

#한 글자인 단어와, stopwords로 불필요한 단어 제거하기

for i in range(len(X)):  #i는 각각의 문장들
  result = []
  for j in range(len(X[i])):  #j는 각 문장 안 단어들
    if len(X[i][j]) > 1:  #한글자인 단어들은 if문 안에 못들어간다
      if X[i][j] not in list(stopwords['stopword']):
        result.append(X[i][j])   #통과된 텍스트를 빈 리스트에 넣어주기
  X[i] = ' '.join(result)  #문장 별 리스트 요소들을 join으로 이어준다

print(X)

#토크나이징 작업하기(숫자로 라벨화 작업)

token = Tokenizer()
token.fit_on_texts(X) # 어떤형태소를 무슨 숫자로 만들지 지정
tokened_X = token.texts_to_sequences(X) # 해당 형태소를 라벨링 된 숫자로 변경
print(tokened_X[0])

#토큰 저장하기(학습한 문장을 라벨을 붙였기에 그대로 저장해준다)

with open('/content/datasets/books_token.pickle', 'wb') as f:
  pickle.dump(token,f)

wordsize = len(token.word_index) +1 #각 단어 별 붙여진 번호를 볼 수 있다,1은 나중에 0을 포함하려고
print(wordsize)

#문장별로 단어의 갯수가 달라서 맞춰주기

max = 0
for i in range(len(tokened_X)):
  if max < len(tokened_X[i]):  #문장을 하나하나 꺼내서 길이를 보면서 가장 큰 문장을 찾아준다
    max = len(tokened_X[i])  #가장 긴 문장을 다시 max값으로 지정

print(max)  #최대 문장 길이= 970

X_pad = pad_sequences(tokened_X, max) #토큰의 개수가 970개가 되게끔 알아서 앞쪽에 0을 붙여준다
print(X_pad[:10])

#훈련, 결과 데이터 나눠서 저장

X_train, X_test, Y_train, Y_test = train_test_split(
    X_pad, onehot_Y, test_size=0.15
)

print(X_train.shape)
print(X_test.shape)
print(Y_train.shape)
print(Y_test.shape)

#나눈 데이터 저장하기

xy = X_train, X_test, Y_train, Y_test
np.save('/content/datasets/books_data_max_{}_size_{}'.format(max,wordsize), xy)

