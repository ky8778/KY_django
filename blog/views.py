from django.shortcuts import render
from .models import Post

# Create your views here.
def index(request):
    # posts = Post.objects.all()      # Query로 데이터를 가져오는 방법
    posts = Post.objects.all().order_by('-pk')      # pk 값의 역순 (생성 기준 최신 글 부터 보여줌)
    
    postsDict = {
        'posts': posts,
    }

    return render(request, 'blog/index.html', postsDict)   # index.html 파일 렌더링