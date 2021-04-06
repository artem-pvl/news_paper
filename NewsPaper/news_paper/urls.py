from django.urls import path
from .views import NewsList, NewsDetail, PostsFiltered

urlpatterns = [
    path('', NewsList.as_view()),
    path('<int:pk>', NewsDetail.as_view()),
    path('search/', PostsFiltered.as_view())
]
