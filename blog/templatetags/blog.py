# テンプレートタグの作成
from django import template

from django.db.models import Count, Q
from blog.models import Category, Tag, Post, Creation


register = template.Library()

@register.simple_tag
def replace(request, key, value):
    url_dict = request.GET.copy()
    url_dict[key] = value
    return url_dict.urlencode()


@register.inclusion_tag('blog/snippets/sidebar.html', takes_context=True)
def render_sidebar(context, page_type='blog'):
    request = context['request']
    # サイドバーのレンダリング
    # ページタイプ（'blog' or 'portfolio'）により、表示するカテゴリとタブを切り替え
    if page_type == 'portfolio':
        model = Creation
        category_name = 'category-creation-list'
        tag_name = 'tag-creation-list'
    else:
        model = Post
        category_name = 'category-post-list'
        tag_name = 'tag-post-list'

    related_name = model.__name__.lower()

    if request.user.is_authenticated:
        count_obj = Count(related_name)
    else:
        count_obj = Count(related_name, filter=Q(**{f'{related_name}__is_published': True}))
    
    categories = Category.objects.annotate(
        count = count_obj
    ).filter(count__gt=0)

    tag_filter = {}
    if not request.user.is_authenticated:
        tag_filter = {f'{related_name}__is_published': True}

    tags = Tag.objects.filter(
        **{f'{related_name}__is_published': True}).distinct()
    
    return {
        'categories': categories,
        'tags': tags,
        'category_name': category_name,
        'tag_name': tag_name,
    }
    