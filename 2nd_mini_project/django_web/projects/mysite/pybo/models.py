from django.db import models


class Article(models.Model):
    title = models.CharField('종목', max_length=126)
    content = models.TextField('내용')
    #auther = models.CharField('작성자', max_length=16, null=False)
    created_at = models.DateTimeField('작성일')


class Stock(models.Model):
    title = models.CharField('종목', max_length=126)
    content = models.TextField('내용')
    created_at = models.DateTimeField('작성일')

class Cluster(models.Model):
    title = models.CharField('종목', max_length=126)
    content = models.TextField('내용')
    created_at = models.DateTimeField('작성일')


class StockData(models.Model):
    title = models.CharField(max_length=200)
    link = models.URLField()

class Stockinfo(models.Model):
    TransactionDate = models.CharField(max_length=200)
    ReportedDateTime = models.CharField(max_length=200)
    Company = models.CharField(max_length=200)
    Symbol = models.CharField(max_length=200)
    InsiderRelationship = models.CharField(max_length=200)
    SharesTraded = models.CharField(max_length=200)
    AveragePrice = models.CharField(max_length=200)
    TotalAmount = models.CharField(max_length=200)
    SharesOwned = models.CharField(max_length=200)
    Type = models.CharField(max_length=200)

class Clusterinfo(models.Model):
    FilingDate = models.CharField(max_length=200)
    FilingTime = models.CharField(max_length=200)
    TradeDate = models.CharField(max_length=200)
    Ticker = models.CharField(max_length=200)
    CompanyName = models.CharField(max_length=200)
    Industry = models.CharField(max_length=200)
    TradeType = models.CharField(max_length=200)
    Price = models.CharField(max_length=200)
    Qty = models.CharField(max_length=200)
    Owned = models.CharField(max_length=200)
    Value = models.CharField(max_length=200)