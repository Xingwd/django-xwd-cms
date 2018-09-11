'''
相关资料：
https://docs.djangoproject.com/zh-hans/2.0/topics/http/views/
'''

from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.shortcuts import get_object_or_404, render

from .models import Category, Column, Article


def index(request):
    categories = Category.objects.all()
    nav_display_columns = Column.objects.filter(nav_display=True)
    return render(request, 'index.html', {
        'categories': categories,
        'nav_display_columns': nav_display_columns,
    })


# def column_detail(request, column_slug):
#     column = get_object_or_404(Column, slug=column_slug)
#
#     article_list = column.article_set.all()
#     paginator = Paginator(article_list, 1)  # Show 25 contacts per page
#
#     page = request.GET.get('page')
#     article_page = paginator.get_page(page)
#
#     return render(request, 'tinysite/column.html', {
#         'column': column,
#         'article_page': article_page,
#     })


def article_detail(request, category_slug, column_slug, article_slug):
    category = get_object_or_404(Category, slug=category_slug)
    column = get_object_or_404(Column, slug=column_slug)
    article = get_object_or_404(Article, slug=article_slug)

    # 浏览量 +1
    article.increase_views()

    article_list = [ a for a in Article.objects.filter(column=column.id) ]
    current_article_index = article_list.index(article)

    if len(article_list) < 2:
        previous_article = None
        next_article = None

    else:
        if current_article_index == 0:
            previous_article = None
            next_article = article_list[1]

        elif current_article_index > 0 and current_article_index < len(article_list) - 1:
            previous_article = article_list[current_article_index - 1]
            next_article = article_list[current_article_index + 1]
        else:
            previous_article = article_list[current_article_index - 1]
            next_article = None

    return render(request, 'tinysite/article.html', {
        'category': category,
        'column': column,
        'article': article,
        'previous_article': previous_article,
        'next_article': next_article,
    })
