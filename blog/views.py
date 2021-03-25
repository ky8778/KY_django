from django.shortcuts import render
from .models import Post

# Create your views here.
def index(request):
    # posts = Post.objects.all()      # Query로 데이터를 가져오는 방법
    posts = Post.objects.all().order_by('-pk')      # pk 값의 역순 (생성 기준 최신 글 부터 보여줌)
    
    my_posts = {
        'posts': posts,
    }

    return render(request, 'blog/index.html', my_posts)   # index.html 파일 렌더링

def single_post_page(request, pk):
    post = Post.objects.get(pk=pk)
    my_post = {
        'post': post,
    }

    return render(request, 'blog/single_post_page.html', my_post)