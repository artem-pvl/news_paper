from django.urls import path
from .views import NewsList, NewsDetail, PostsFiltered, PostAdd, PostEdit,\
    PostDelete, author_me

urlpatterns = [
    path('', NewsList.as_view()),
    path('<int:pk>', NewsDetail.as_view()),
    path('search/', PostsFiltered.as_view()),
    path('add/', PostAdd.as_view(), name='news_add'),
    path('<int:pk>/edit/', PostEdit.as_view(), name='news_edit'),
    path('<int:pk>/delete/', PostDelete.as_view(), name='news_delete'),
    path('setauthor/', author_me, name='author_me'),
]
