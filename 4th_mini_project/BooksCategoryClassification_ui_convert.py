"""
books category classification GUI
tensorflow version: 2.3.0
"""
import pickle
import sys


import pandas as pd
import numpy as np
from eunjeon import Mecab
from PyQt5 import uic
from PyQt5.QtCore import QPointF
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import *
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences

# ui 파일 로드
form_window = uic.loadUiType("./mainwindow.ui")[0]

# QWidget과 ui 파일을 상속받은 클래스
class Exam(QWidget, form_window):
    def __init__(self):
        """객체 초기화"""
        super().__init__()  # 부모의 생성자 실행
        self.path = None
        self.setupUi(self)
        self.set_font(self.InputText, "Yummo,나눔바른펜")
        self.InputText.textChanged.connect(self.init_textedit)
        # 그림자 생성
        self.set_shadow(self.InputText)
        self.set_shadow(self.Result)
        self.set_shadow(self.History)
        # 파일 로드
        self.load_pickles()

        # 위 사각형 클릭 시 textedit 초기화
        self.reset_1.clicked.connect(self.clear_text)
        self.reset_2.clicked.connect(self.clear_text)
        # 버튼 클릭 시 예측
        self.Predict.clicked.connect(self.predict)

    def set_shadow(self, object):
        """해당 객체에 그림자 생성"""
        shadow = QGraphicsDropShadowEffect()
        shadow.setOffset(QPointF(5.0, 6.0))
        shadow.setColor(QColor(155, 155, 155, 155))
        shadow.setBlurRadius(33)
        object.setGraphicsEffect(shadow)

    def init_textedit(self):
        self.InputText.setFontFamily("Yummo,나눔바른펜")
        self.InputText.setTextColor(QColor(52, 52, 52, 255))

    def load_pickles(self):
        """모델 및 예측에 필요한 파일들 로드"""
        # 모델 로드
        self.model = load_model("./models/books_classification_0.9008.h5")
        # 한글 분석기 로드
        self.mecab = Mecab()
        self.max = 612
        # one-hot encoder 로드
        with open(
            "./data/nouns_category_onehot_encoder.pickle",
            "rb",
        ) as f:
            encoder = pickle.load(f)
        self.category = encoder.categories_[0]
        self.counts = {cat: 0 for cat in self.category}
        # Tokenizer 로드
        with open("./data/nouns_token.pickle", "rb") as f:
            self.token = pickle.load(f)
        # stopword 로드
        self.stopwords = pd.read_csv("./data/stopwords.csv", index_col=0)

    def set_font(self, object, string):
        font = object.font()
        font.setFamily(string)
        print(type(font))
        object.setFont(font)

    def clear_text(self):
        """textedit 초기화"""
        self.InputText.clear()

    def delete_stopwords(self, lst):
        """해당 list의 stopword 제거한 string 반환"""
        words = [
            word for word in lst if word not in list(self.stopwords["stopword"]) and len(word) > 1
        ]
        return " ".join(words)

    def predict(self):
        """textedit의 글자를 통해 예측"""
        # textedit의 글자를 가져와 명사 추출
        target_raw = self.InputText.toPlainText()
        target_nouns = self.mecab.nouns(target_raw)
        n = self.delete_stopwords(target_nouns)
        nouns = []
        nouns.append(n)

        # 해당 글자 토큰화
        nouns_tokened = self.token.texts_to_sequences(nouns)
        nouns_pad = pad_sequences(nouns_tokened, self.max)

        # 결과 예측 및 출력
        predict = self.model.predict(nouns_pad)
        if predict.max() >= 0.5:
            target = self.category[np.argmax(predict)]
            self.counts[target] += 1
            result = f"It's book about {target}.\nThank you! The kids will be happy."
            self.Result.setText(result)
        else:
            self.Result.setText("Please give me a little more details")
            self.set_font(self.Result, "Yummo,나눔바른펜")
        history = {f"{key}": f"{self.counts[key]}" for key in self.counts if self.counts[key] > 0}
        print(history)
        self.History.setText("\n".join(history.keys()))
        self.HistoryNumber.setText("\n".join(history.values()))


# 현재 py 파일의 절대경로를 인수로 QApplication 객체 생성
app = QApplication(sys.argv)

# ui 파일을 상속받은 QWidget 클래스를 띄움
mainWindow = Exam()
mainWindow.show()

# AQpplication 객체에서 이벤트 루프를 실행하고, 윈도우 x 버튼 클릭 시 종료함
sys.exit(app.exec_())
