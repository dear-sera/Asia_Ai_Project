from django.shortcuts import render,redirect, get_object_or_404
from django.http import HttpResponse
from pybo.models import Article, StockData, Stock, Cluster, Stockinfo, Clusterinfo
from pybo.forms import ArticleForm, StockForm, ClusterForm
from django.utils import timezone
from django.core.paginator import Paginator
from django.template import loader
import pandas as pd
from . import clusterinfo, kospi, us_tele
from .kospi import parsingStockInfo, sendMessage
from .us_tele import msg_text

def kospi(request):
    parsingStockInfo
    data = sendMessage(parsingStockInfo())
    return redirect('pybo:index')

def apple(request):
    msg_text('apple')
    return redirect('pybo:index')

def ama(request):
    msg_text('amazon')
    return redirect('pybo:index')


def cou(request):
    msg_text('coupang')
    return redirect('pybo:index')

def dat(request):
    msg_text('datadog')
    return redirect('pybo:index')

def tes(request):
    msg_text('tesla')
    return redirect('pybo:index')

def pal(request):
    msg_text('palantir')
    return redirect('pybo:index')



def index(request):
    return render(request, 'pybo/home.html')


"""
    pybo 목록 출력
    page = request.GET.get('page', '1')
    article_list = Article.objects.order_by('-created_at')
    paginator = Paginator(article_list, 10)
    page_obj = paginator.get_page(page)
    context = {'article_list': page_obj}
    return render(request, 'pybo/article_list.html', context)
"""


def cluster(request):
    # pybo 내용 출력

    #page = request.GET.get('page', '1')  # 페이지 요청 url에서 page파라미터가 있으면 값을 반환, 없으면 1이 반환된다
    cluster_list = Clusterinfo.objects.order_by()  # order_by -가 붙으면 내림차순으로 정렬

    url = 'http://openinsider.com/latest-cluster-buys'
    soup = clusterinfo.get_soup(url)
    col, data = clusterinfo.get_df_data_on_site(soup)
    df = clusterinfo.make_refine_df(col, data)
    data = df.values.tolist()
    print(data)
    context = {'cluster_list': data}
    return render(request, 'pybo/cluster.html', context)

def stock(request):
    # pybo 내용 출력

    page = request.GET.get('page', '1')  # 페이지 요청 url에서 page파라미터가 있으면 값을 반환, 없으면 1이 반환된다
    # Django는 Django 모델 클래스에 대해 "objects" 라는 Manager 객체를 자동 추가
    stock_list = Stockinfo.objects.order_by()

    # paginator개체 생성하면서 페이지 처리 객체 생성, 페이지당 보여줄 게시물 개수 설정
    #paginator = Paginator(stock_list, 10)
    #page_obj = paginator.get_page(page)
    df = pd.read_excel('D:/AI/pjt2/DB/df_apple.21.05.05.18.31.xlsx')
    df = df[::-1]
    data = df.values.tolist()

    context = {'stock_list': data}
    # for  idx in range(len(data["TransactionDate"])) :
    #     print( data["TransactionDate"][idx] )

    return render(request, 'pybo/stock.html', context)

def amazon(request):
    df = pd.read_excel('D:/AI/pjt2/DB/df_amazon.21.05.05.17.14.xlsx')
    df = df[::-1]
    data = df.values.tolist()

    context = {'amazon_list': data}
    return render(request, 'pybo/amazon.html', context)

def coupang(request):
    df = pd.read_excel('D:/AI/pjt2/DB/df_coupang.21.03.15.19.00.xlsx')
    df = df[::-1]
    data = df.values.tolist()

    context = {'coupang_list': data}
    return render(request, 'pybo/coupang.html', context)

def datadog(request):
    df = pd.read_excel('D:/AI/pjt2/DB/df_datadog.21.05.05.18.05.xlsx')
    df = df[::-1]
    data = df.values.tolist()

    context = {'datadog_list': data}
    return render(request, 'pybo/datadog.html', context)

def palantir(request):
    df = pd.read_excel('D:/AI/pjt2/DB/df_palantir.21.05.05.20.04.xlsx')
    df = df[::-1]
    data = df.values.tolist()

    context = {'palantir_list': data}
    return render(request, 'pybo/palantir.html', context)

def tesla(request):
    df = pd.read_excel('D:/AI/pjt2/DB/df_tesla.21.04.29.20.20.xlsx')
    df = df[::-1]
    data = df.values.tolist()

    context = {'tesla_list': data}
    return render(request, 'pybo/tesla.html', context)

def unity(request):
    df = pd.read_excel('D:/AI/pjt2/DB/df_unity.21.05.04.16.45.xlsx')
    df = df[::-1]
    data = df.values.tolist()

    context = {'unity_list': data}
    return render(request, 'pybo/unity.html', context)

def detail(request, article_id):
    
    #pybo 내용 출력

    article = get_object_or_404(Article, pk=article_id)
    context = {'article': article}
    return render(request, 'pybo/article_detail.html', context)


def details(request, article_id):
    # pybo 내용 출력

    cluster = get_object_or_404(Cluster, pk=article_id)
    context = {'cluster': cluster}
    return render(request, 'pybo/cluster_detail.html', context)



def cluster_create(request):
    """
    pybo 거래등록
    """
    if request.method == 'POST':
        form = ClusterForm(request.POST)
        if form.is_valid():
            cluster = form.save(commit=False)
            cluster.created_at = timezone.now()
            cluster.save()
            return redirect('pybo:cluster')
    else:
        form = ClusterForm()
    context = {'form': form}
    return render(request, 'pybo/cluster_form.html', context)

def stock_create(request):
    """
    pybo 거래등록
    """
    if request.method == 'POST':
        form = StockForm(request.POST)
        if form.is_valid():
            stock = form.save(commit=False)
            stock.created_at = timezone.now()
            stock.save()
            return redirect('pybo:stock')
    else:
        form = StockForm()
    context = {'form': form}
    return render(request, 'pybo/stock_form.html', context)


#if __name__ = '__main__':
#    amazon()
