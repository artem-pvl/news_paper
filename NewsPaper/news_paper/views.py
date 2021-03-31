# from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Post


class NewsList(ListView):
    model = Post
    template_name = 'newses.html'
    context_object_name = 'newses'
    queryset = Post.objects.order_by('-creation_time').filter(type=Post.NEWS).values()


class NewsDetail(DetailView):
    model = Post
    template_name = 'news.html'
    context_object_name = 'news'
    queryset = Post.objects.filter(type=Post.NEWS).values()

# Create your views here.
