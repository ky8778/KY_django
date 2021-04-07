from django.urls import path
from . import views

urlpatterns = [
    # [FBV] blog/ url에서 import한 views.py에 있는 index() 함수를 실행한다.
    # path('', views.index),
    # path('<int:pk>/', views.single_post_page),
    
    # [CBV] ListView를 사용할 때는 '_list' 가 붙은 html 파일을 기본 템플릿으로 사용하도록 되어있다.
    # 방법1. PostList Class에서 template_name을 직접 지정하는 방법
    # 방법2. post_list.html을 만드는 방법
    path('', views.PostList.as_view()),
    path('<int:pk>/', views.PostDetail.as_view()),
    path('category/<str:slug>/', views.category_page),
    path('tag/<str:slug>/', views.tag_page),
    path('create_post/', views.PostCreate.as_view()),
]