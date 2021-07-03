from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Post, Category

# Create your views here.
''' CBV '''
class PostList(ListView):
    model = Post
    # default template : <app_label>/<model_name>_list.html
    template_name = 'blog/blog.html' 
	# default context name : object_list
    context_object_name = 'posts'
    ordering = '-pk'

    # ListView를 상속받은 PostList에서 model = Post 로 선언하면
    # get_context_data 에서 post_list = Post.objects.all() 을 명령함
    # Template 에서 {% for p in post_list %} 와 같이 사용가능
    # context 커스텀해서 사용하기
    def get_context_data(self, **kwargs):
        context = super(PostList, self).get_context_data()
        context['categories'] = Category.objects.all()
        context['no_category_post_count'] = Post.objects.filter(category=None).count()
        return context

class PostDetail(DetailView):
    model = Post
    template_name = 'blog/single_post_page.html' 
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super(PostDetail, self).get_context_data()
        context['categories'] = Category.objects.all()
        context['no_category_post_count'] = Post.objects.filter(category=None).count()
        return context

''' FBV '''
def index(request):
    posts = Post.objects.all().order_by('-pk')
    context = {
        'posts': posts,
    }
    return render(request, 'blog/index.html', context)
    
def single_post_page(request, pk):
    post = Post.objects.get(pk=pk)
    context = {
        'post': post
    }
    return render(request, 'blog/single_post_page.html', context)

def category_page(request, slug):
    if slug == 'no_category':
        category = '미분류'
        posts = Post.objects.filter(category=None)
    else:
        category = Category.objects.get(slug=slug)
        posts = Post.objects.filter(category=category)
        
    context = {
        'posts': posts,
        'categories': Category.objects.all(),
        'no_category_post_count': Post.objects.filter(category=None).count(),
        'category': category,
    }
    return render(request, 'blog/blog.html', context)
