from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Post

# Create your views here.
''' CBV '''
class PostList(ListView):
    model = Post
    # default template : <app_label>/<model_name>_list.html
    template_name = 'blog/blog.html' 
	# default context name : object_list
    context_object_name = 'posts'
    ordering = '-pk'

class PostDetail(DetailView):
    model = Post
    template_name = 'blog/single_post_page.html' 
    context_object_name = 'post'

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