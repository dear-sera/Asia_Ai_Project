from django import forms
from pybo.models import Article, Stock, Cluster


class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'content']
        labels = {
            'title': '종목',
            'content': '내용',
        }



class StockForm(forms.ModelForm):
    class Meta:
        model = Stock
        fields = ['title', 'content']
        labels = {
            'title': '종목',
            'content': '내용',
        }

class ClusterForm(forms.ModelForm):
    class Meta:
        model = Cluster
        fields = ['title', 'content']
        labels = {
            'title': '종목',
            'content': '내용',
        }

