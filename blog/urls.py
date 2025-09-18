from django.urls import path

from blog.views import (
    HomeView,
    PostListView,
    PostDetailView,
    CategoryPostListView,
    TagPostListView,
    SearchPostListView,
    CreationListView,
    CreationDetailView,
    CategoryCreationListView,
    TagCreationListView,
    SearchCreationListView,
)


urlpatterns = [
    # ホーム画面
    path('', HomeView.as_view(), name='home'),
    
    # ブログ
    path('blog/', PostListView.as_view(), name='post-list'),
    path('blog/post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('blog/category/<str:slug>/', CategoryPostListView.as_view(), name='category-post-list'),
    path('blog/tag/<str:slug>/', TagPostListView.as_view(), name='tag-post-list'),
    path('blog/search/', SearchPostListView.as_view(), name='search-post-list'),

    # ポートフォリオ
    path('portfolio/', CreationListView.as_view(), name='creation-list'),
    path('portfolio/<int:pk>/', CreationDetailView.as_view(), name='creation-detail'),
    path('portfolio/category/<str:slug>/', CategoryCreationListView.as_view(), name='category-creation-list'),
    path('portfolio/tag/<str:slug>/', TagCreationListView.as_view(), name='tag-creation-list'),
    path('portfolio/search/', SearchCreationListView.as_view(), name='search-creation-list'),
]
