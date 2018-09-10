# -*- coding: UTF-8 -*-
from django.contrib import admin

from .models import Category, Column, Article


class CategoryAdmin(admin.ModelAdmin):
    fieldsets = [
        ('分类名称', {'fields': ['name']}),
    ]

    list_display = ('name',)


class ColumnAdmin(admin.ModelAdmin):
    fieldsets = [
        ('栏目名称', {'fields': ['name', 'nav_display']}),
        ('所属分类', {'fields': ['category']}),
        ('栏目网址', {'fields': ['slug']}),
        ('栏目介绍', {'fields': ['intro']}),
    ]

    list_display = ('name', 'category', 'slug', 'intro', 'nav_display')


class ArticleAdmin(admin.ModelAdmin):
    fieldsets = [
        ('标题', {'fields': ['title']}),
        ('所属栏目', {'fields': ['column']}),
        ('网址', {'fields': ['slug']}),
        ('内容', {'fields': ['content']}),
    ]

    list_display = ('title', 'column', 'slug', 'views', 'pub_time', 'update_time')

    list_filter = ['column']

    search_fields = ['title']


admin.site.register(Category, CategoryAdmin)
admin.site.register(Column, ColumnAdmin)
admin.site.register(Article, ArticleAdmin)