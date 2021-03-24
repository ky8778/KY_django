from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),  # blog/ url에서 import한 views.py에 있는 index() 함수를 실행한다.
]