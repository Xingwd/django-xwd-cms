'''
相关资料：
https://docs.djangoproject.com/zh-hans/2.0/topics/http/urls/
'''

from django.urls import path

from . import views

app_name = 'tinysite'
urlpatterns = [
    path('', views.index, name='index'),
    # path('column/<slug:column_slug>/', views.column_detail, name='column'),
    path('column/<slug:column_slug>/<slug:article_slug>', views.article_detail, name='article'),
]