from .models import Post
# [FBV]
from django.shortcuts import render
# [CBV]
from django.views.generic import ListView, DetailView

# Create your views here.
# CBV
class PostList(ListView):
    model = Post
    # 방법1
    # template_name = 'blog/index.html'
    # 방법2는 html 파일을 _list로 (대소문자는 구분 안하는 것 같네)
    ordering = '-pk'

class PostDetail(DetailView):
    model = Post
    template_name = 'blog/single_post_page.html'

''' FBV
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
'''