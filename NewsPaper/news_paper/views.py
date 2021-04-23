# from django.shortcuts import render
from django.views.generic import ListView, DetailView, UpdateView, DeleteView,\
    CreateView
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Post
from .filters import PostFilter
from .forms import PostForm

from django.shortcuts import redirect
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required


class NewsList(ListView):
    model = Post
    template_name = 'newses.html'
    context_object_name = 'newses'
    ordering = '-creation_time'
    paginate_by = 10


class NewsDetail(DetailView):
    model = Post
    template_name = 'news.html'
    context_object_name = 'news'
    queryset = Post.objects.filter(type=Post.NEWS).values()


class PostsFiltered(ListView):
    model = Post
    template_name = 'search.html'
    context_object_name = 'search_post'
    ordering = ['-creation_time']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = PostFilter(self.request.GET,
                                       queryset=self.get_queryset())
        return context


class PostAdd(CreateView):
    model = Post
    template_name = 'add.html'
    form_class = PostForm
    success_url = '/news/'


class PostEdit(LoginRequiredMixin, UpdateView):
    model = Post
    template_name = 'add.html'
    form_class = PostForm
    success_url = '/news/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_author'] = not self.request.user.groups.\
            filter(name='authors').exists()
        return context


class PostDelete(DeleteView):
    model = Post
    template_name = 'delete.html'
    queryset = Post.objects.all()
    success_url = '/news/'


@login_required
def author_me(request):
    user = request.user
    premium_group = Group.objects.get(name='authors')
    if not request.user.groups.filter(name='authors').exists():
        premium_group.user_set.add(user)
    return redirect('/news')

# Create your views here.
