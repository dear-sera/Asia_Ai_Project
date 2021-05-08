from django.urls import path
from django.contrib import admin
from django.http import HttpResponse
from .views import base_views


app_name = 'pybo'

def home(request):
    return HttpResponse('Home Page')

urlpatterns = [
    #path('', home),
    path('', base_views.index, name='index'),
    path('<int:article_id>/', base_views.detail, name='detail'),
    path('<int:article_id>/', base_views.details, name='details'),
    path('cluster/', base_views.cluster, name='cluster'),
    path('stock/', base_views.stock, name='stock'),
    path('amazon/', base_views.amazon, name='amazon'),
    path('coupang/', base_views.coupang, name='coupang'),
    path('datadog/', base_views.datadog, name='datadog'),
    path('palantir/', base_views.palantir, name='palantir'),
    path('tesla/', base_views.tesla, name='tesla'),
    path('unity/', base_views.unity, name='unity'),
    path('article/create/', base_views.cluster_create, name='cluster_create'),
    path('stock/create/', base_views.stock_create, name='stock_create'),
    path('kospi/', base_views.kospi, name='kospi'),
    path('apple/', base_views.apple, name='apple'),
    path('ama/', base_views.ama, name='ama'),
    path('cou/', base_views.cou, name='cou'),
    path('dat/', base_views.dat, name='dat'),
    path('tes/', base_views.tes, name='tes'),
    path('pal/', base_views.pal, name='pal'),
]