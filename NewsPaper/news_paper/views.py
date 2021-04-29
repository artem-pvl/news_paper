# from django.shortcuts import render
from django.views.generic import ListView, DetailView, UpdateView, DeleteView,\
    CreateView
from django.contrib.auth.mixins import LoginRequiredMixin,\
    PermissionRequiredMixin

from .models import Category, Post, PostCategory, Mailing
from .filters import PostFilter
from .forms import PostForm

from django.shortcuts import redirect
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model


class NewsList(ListView):
    model = Post
    template_name = 'newses.html'
    context_object_name = 'newses'
    ordering = '-creation_time'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_author'] = not self.request.user.groups.\
            filter(name='authors').exists()
        return context


class NewsDetail(DetailView):
    model = Post
    template_name = 'news.html'
    context_object_name = 'news'
    # queryset = Post.objects.filter(type=Post.NEWS).values()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = list(PostCategory.objects.filter(
            post=self.kwargs['pk']).values('category', 'category__category'))
        sub = list(Mailing.objects.filter(subscribers=self.request.user.id).
                   values('category'))
        context['subscribed'] = [s['category'] for s in sub]
        return context


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


class PostAdd(PermissionRequiredMixin, CreateView):
    model = Post
    template_name = 'add.html'
    form_class = PostForm
    success_url = '/news/'
    permission_required = ('news_paper.add_post',)


class PostEdit(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Post
    template_name = 'add.html'
    form_class = PostForm
    success_url = '/news/'
    permission_required = ('news_paper.change_post',)


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


@login_required
def subscribe_me(request, pk):
    if not Mailing.objects.check(subscribers=get_user_model().
                                 objects.get(id=request.user.id),
                                 category=Category.objects.get(id=pk)):
        Mailing.objects.create(subscribers=get_user_model().
                               objects.get(id=request.user.id),
                               category=Category.objects.get(id=pk))
    return redirect('/news')

# Create your views here.
