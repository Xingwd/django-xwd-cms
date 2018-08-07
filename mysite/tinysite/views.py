from django.views import generic

from .models import Category, Course


class IndexView(generic.ListView):
    model = Category
    template_name = 'tinysite/index.html'


class CourseView(generic.DetailView):
    model = Course
    template_name = 'tinysite/course.html'