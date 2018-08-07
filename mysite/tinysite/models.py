from django.db import models



class Category(models.Model):
    category_name = models.CharField(max_length=200)

    def __str__(self):
        return self.category_name


class Course(models.Model):
    category = models.ForeignKey(Category, null=True, blank=True, on_delete=models.SET_NULL)
    course_name = models.CharField(max_length=200)
    course_description = models.TextField()

    def __str__(self):
        return self.course_name


class Chapter(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    chapter_title = models.CharField(max_length=200)
    chapter_content = models.TextField()

    def __str__(self):
        return self.chapter_title