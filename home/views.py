from django.shortcuts import render
from blog.models import Post

# Create your views here.
def home(request):
    recent_posts = Post.objects.order_by('-pk')[:3]
    context = {
        'recent_posts': recent_posts,
    }
    return render(request, 'home/home.html', context)

def about_me(request):
    return render(request, 'home/about_me.html')