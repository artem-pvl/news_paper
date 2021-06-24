from django.contrib import admin
from modeltranslation.admin import TranslationAdmin
from .models import Mailing, Post, Comment, Author, Category, PostCategory

admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Author)
admin.site.register(Category)
admin.site.register(PostCategory)
admin.site.register(Mailing)


class CategoryAdmin(TranslationAdmin):
    model = Category


class PostAdmin(TranslationAdmin):
    model = Post


class CommentAdmin(TranslationAdmin):
    model = Comment


# Register your models here.
