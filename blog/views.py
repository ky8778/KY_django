from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Post, Category, Tag
from .forms import CommentForm
from django.core.exceptions import PermissionDenied
from django.utils.text import slugify


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
        context['comment_form'] = CommentForm
        return context


# python은 class에서 Mixin을 사용하면 다른 클래스의 메서드를 추가할 수 있음
class PostCreate(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Post
    fields = ['title', 'hook_text', 'content', 'head_image', 'file_upload', 'category']
   
    # default template name : blog/post_form.html

    def test_func(self):
        return self.request.user.is_superuser or self.request.user.is_staff

    # default form_valid 재정의, login한 author 없으면 redirect
    # form_valid : form 안에 들어온 값을 바탕으로 모델에 해당하는 인스턴스를 만들어 DB에 저장한 뒤
    # 해당 인스턴스의 경로로 리다이렉트하는 역할
    def form_valid(self, form):
        current_user = self.request.user
        if current_user.is_authenticated and (current_user.is_staff or current_user.is_superuser):
            form.instance.author = current_user
            response = super(PostCreate, self).form_valid(form)

            tags_str = self.request.POST.get('tags_str')
            if tags_str:
                tags_str = tags_str.strip()
                tags_str = tags_str.replace(',', ';')
                tags_list = tags_str.split(';')

                for t in tags_list:
                    t = t.strip()
                    tag, is_tag_created = Tag.objects.get_or_create(name=t)
                    if is_tag_created:
                        tag.slug = slugify(t, allow_unicode=True)
                        tag.save()
                    self.object.tags.add(tag)
            return response
        else:
            return redirect('/blog/')


class PostUpdate(LoginRequiredMixin, UpdateView):
    model = Post
    fields = ['title', 'hook_text', 'content', 'head_image', 'file_upload', 'category']
    
    # default template name : blog/post_form.html
    template_name = 'blog/post_update_form.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user == self.get_object().author:
            # self.get_object().author 는 Post.objects.get(pk=pk) 와 동일한 기능
            return super(PostUpdate, self).dispatch(request, *args, **kwargs)
        else:
            # 403 Error Throw
            raise PermissionDenied
    
    # CBV 로 View를 만들 때 Template으로 인자를 넘길 땐 get_context_data() 를 이용
    def get_context_data(self, **kwargs):
        context = super(PostUpdate, self).get_context_data()
        if self.object.tags.exists():
            tags_str_list = list()
            for t in self.object.tags.all():
                tags_str_list.append(t.name)
            context['tags_str_default'] = '; '.join(tags_str_list)
        
        return context

    def form_valid(self, form):
        response = super(PostUpdate, self).form_valid(form)
        self.object.tags.clear()
        
        tags_str = self.request.POST.get('tags_str')
        if tags_str:
            tags_str = tags_str.strip()
            tags_str = tags_str.replace(',', ';')
            tags_list = tags_str.split(';')

            for t in tags_list:
                t = t.strip()
                tag, is_tag_created = Tag.objects.get_or_create(name=t)
                if is_tag_created:
                    tag.slug = slugify(t, allow_unicode=True)
                    tag.save()
                self.object.tags.add(tag)
        return response


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

def tag_page(request, slug):
    tag = Tag.objects.get(slug=slug)
    posts = tag.post_set.all()

    context = {
        'posts': posts,
        'tag': tag,
        'categories': Category.objects.all(),
        'no_category_post_count': Post.objects.filter(category=None).count(),
    }

    return render(request, 'blog/blog.html', context)

def new_comment(request, pk):
    # View 에서 로그인 되었을 떄만 하도록 만들어두었으나,
    # 비정상적으로 접근을 시도할 수도 있음.
    # 이런 경우 PermissionDenied 발생
    if request.user.is_authenticated:
        post = get_object_or_404(Post, pk=pk)   # pk가 없을 경우 404 error 발생

        if request.method == 'POST':
            comment_form = CommentForm(request.POST)
            if comment_form.is_valid():
                comment = comment_form.save(commit=False)
                comment.post = post
                comment.author = request.user
                comment.save()
                return redirect(comment.get_absolute_url())
        else:
            return redirect(post.get_absolute_url())
    else:
        raise PermissionDenied