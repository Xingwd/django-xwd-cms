# -*- coding: UTF-8 -*-
from django.contrib import admin

from .models import Category, Course, Chapter


class CategoryAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['category_name']}),
    ]


class ChapterInline(admin.StackedInline):
    model = Chapter
    extra = 0
    #classes = ['collapse']


class CourseAdmin(admin.ModelAdmin):
    fieldsets = [
        ('教程名称', {'fields': ['course_name']}),
        ('教程分类', {'fields': ['category']}),
        ('教程描述', {'fields': ['course_description']})
    ]

    inlines = [ChapterInline]

    list_display = ('course_name', 'category', 'course_description')

    list_filter = ['category']

    search_fields = ['course_name']


admin.site.register(Category, CategoryAdmin)
admin.site.register(Course, CourseAdmin)