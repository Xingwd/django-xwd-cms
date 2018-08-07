from django.urls import path

from . import views

app_name = 'tinysite'
urlpatterns = [
    # ex: /tinysite/
    path('', views.IndexView.as_view(), name='index'),
    # ex: /tinysite/1/
    path('<int:pk>/', views.CourseView.as_view(), name='course'),
]