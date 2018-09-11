# -*- coding: utf-8 -*-
'''
相关资料：
https://docs.djangoproject.com/zh-hans/2.0/topics/db/models/
https://docs.djangoproject.com/zh-hans/2.0/topics/db/queries/
'''

from django.db import models
from django.urls import reverse


class Category(models.Model):
    name = models.CharField('栏目分类', max_length=100)
    slug = models.SlugField('类别网址', max_length=256, db_index=True, default='category')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "栏目分类"
        verbose_name_plural = "栏目分类"


class Column(models.Model):
    category = models.ForeignKey(Category, null=True, blank=True, on_delete=models.SET_NULL, verbose_name = "所属分类")
    name = models.CharField('栏目名称', max_length=100)
    slug = models.SlugField('栏目网址', max_length=256, db_index=True)
    intro = models.TextField('栏目简介', default='')

    nav_display = models.BooleanField('导航显示', default=True)

    def __str__(self):
        return self.name

    # def get_absolute_url(self):
    #     return reverse('tinysite:column', args=[str(self.slug,)])

    class Meta:
        verbose_name = "栏目"
        verbose_name_plural = "栏目"


class Article(models.Model):
    column = models.ForeignKey(Column, on_delete=models.CASCADE, verbose_name = "所属栏目")
    title = models.CharField('标题', max_length=200)
    slug = models.SlugField('网址', max_length=200)
    content = models.TextField('内容', default='')
    pub_time = models.DateTimeField('发表时间', auto_now_add=True)
    update_time = models.DateTimeField('更新时间', auto_now=True, null=True)
    views = models.PositiveIntegerField('浏览量', default=0)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('tinysite:article', args=[self.column.category.slug, self.column.slug, str(self.slug)])

    class Meta:
        verbose_name = "文章"
        verbose_name_plural = "文章"

    # 浏览量增加函数
    def increase_views(self):
        self.views += 1
        self.save(update_fields=['views'])