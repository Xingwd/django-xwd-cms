'''
导航栏上下文
'''

from .models import Category, Column

categories = Category.objects.all()
nav_display_columns = Column.objects.filter(nav_display=True)


def nav(request):
    return {'categories': categories, 'nav_display_columns': nav_display_columns}


