from django_filters import FilterSet
from .models import Post


class PostFilter(FilterSet):
    class Meta:
        model = Post
        fields = {
            'creation_time': ['gt'],
            'author__user_id__username': ['icontains'],
        }
