from django.db.models import Q
from django.http import Http404
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, TemplateView

from blog.models import Post, Category, Tag, Creation

post_per_page = 3

class PostListView(ListView):
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
    paginate_by = post_per_page

    def get_queryset(self):
        posts = super().get_queryset()

        if not self.request.user.is_authenticated:
            posts = posts.filter(is_published=True)

        return posts.order_by('-updated_at')


class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'

    def get_object(self, queryset=None):
        post = super().get_object(queryset)
        # 公開済みorログイン
        if post.is_published or self.request.user.is_authenticated:
            return post
        else:
            raise Http404
        

class CategoryPostListView(ListView):
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
    paginate_by = post_per_page

    def get_queryset(self):
        slug = self.kwargs['slug']
        self.category = get_object_or_404(Category, slug=slug)
        queryset = super().get_queryset().filter(category=self.category)

        if self.request.user.is_authenticated:
            queryset = queryset.filter(is_published=True)

        return  queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.category
        return context
    

class TagPostListView(ListView):
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
    paginate_by = post_per_page

    def get_queryset(self):
        slug = self.kwargs['slug']
        self.tag = get_object_or_404(Tag, slug=slug)
        queryset = super().get_queryset().filter(tags=self.tag)
       
        if self.request.user.is_authenticated:
            queryset = queryset.filter(is_published=True)

        return  queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tag'] = self.tag
        return context
    

class SearchPostListView(ListView):
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
    paginate_by = post_per_page

    def get_queryset(self):
        self.query = self.request.GET.get('query') or ''
        queryset = super().get_queryset()

        if self.query:
            queryset = queryset.filter(
                Q(title__icontains=self.query) | Q(content__icontains=self.query)
            )
        
        if not self.request.user.is_authenticated:
            queryset = queryset.filter(is_published=True)

        self.post_count = len(queryset)

        return  queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.query
        context['post_count'] = self.post_count
        return context
    
#----------------------------------------------------------------------------

creation_per_page = 5

class CreationListView(ListView):
    model = Creation
    template_name = 'portfolio/creation_list.html'
    context_object_name = 'creations'
    paginate_by = creation_per_page

    def get_queryset(self):
        creations = super().get_queryset()

        if not self.request.user.is_authenticated:
            creations = creations.filter(is_published=True)

        return creations.order_by('-updated_at')


class CreationDetailView(DetailView):
    model = Creation
    template_name = 'portfolio/creation_detail.html'

    def get_object(self, queryset=None):
        creation = super().get_object(queryset)
        if creation.is_published or self.request.user.is_authenticated:
            return creation
        else:
            raise Http404
        

class CategoryCreationListView(ListView):
    model = Creation
    template_name = 'portfolio/creation_list.html'
    context_object_name = 'creations'
    paginate_by = creation_per_page

    def get_queryset(self):
        slug = self.kwargs['slug']
        self.category = get_object_or_404(Category, slug=slug)
        queryset = super().get_queryset().filter(category=self.category)

        if not self.request.user.is_authenticated:
            queryset = queryset.filter(is_published=True)

        return  queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.category
        return context
    

class TagCreationListView(ListView):
    model = Creation
    template_name = 'portfolio/creation_list.html'
    context_object_name = 'creations'
    paginate_by = creation_per_page

    def get_queryset(self):
        slug = self.kwargs['slug']
        self.tag = get_object_or_404(Tag, slug=slug)
        queryset = super().get_queryset().filter(tags=self.tag)

        if not self.request.user.is_authenticated:
            queryset = queryset.filter(is_published=True)
       
        return  super().get_queryset().filter(tags=self.tag)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tag'] = self.tag
        return context
    

class SearchCreationListView(ListView):
    model = Creation
    template_name = 'portfolio/creation_list.html'
    context_object_name = 'creations'
    paginate_by = creation_per_page

    def get_queryset(self):
        self.query = self.request.GET.get('query') or ''
        queryset = super().get_queryset()

        if self.query:
            queryset = queryset.filter(
                Q(title__icontains=self.query) | Q(content__icontains=self.query)
            )
        
        if not self.request.user.is_authenticated:
            queryset = queryset.filter(is_published=True)

        self.creation_count = len(queryset)

        return  queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.query
        context['creation_count'] = self.creation_count
        return context
    

#----------------------------------------------------------------------------

class HomeView(TemplateView):
    template_name = 'home/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # 最新のブログ記事を5件取得
        context['posts'] = Post.objects.all().order_by('-created_at')[:5]

        # 最新のポートフォリオ作品を3件取得
        context['creations'] = Creation.objects.all().order_by('-created_at')[:5]

        return context
