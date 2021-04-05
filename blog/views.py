from .models import Post, Category
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

    def get_context_data(self, **kwargs):
        context = super(PostList, self).get_context_data()
        context['categories'] = Category.objects.all()
        context['no_category_post_count'] = Post.objects.filter(category=None).count()
        return context

class PostDetail(DetailView):
    model = Post
    template_name = 'blog/single_post_page.html'

    def get_context_data(self, **kwargs):
        context = super(PostDetail, self).get_context_data()
        context['categories'] = Category.objects.all()
        context['no_category_post_count'] = Post.objects.filter(category=None).count()
        return context

# FBV
def category_page(request, slug):
    if slug == 'no_category':
        category = '미분류'
        post_list = Post.objects.filter(category=None)
    else:
        category = Category.objects.get(slug=slug)
        post_list = Post.objects.filter(category=category)
    context = {
        'post_list': post_list,
        'categories': Category.objects.all(),
        'no_category_post_count': Post.objects.filter(category=None).count(),
        'category': category,
    }

    return render(request, 'blog/post_list.html', context)

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