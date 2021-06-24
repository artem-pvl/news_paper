from modeltranslation.translator import register, TranslationOptions

from .models import Category, Post, Comment


@register(Category)
class CategoryTranslationOptions(TranslationOptions):
    fields = ('category',)


@register(Post)
class PostTranslationOptions(TranslationOptions):
    fields = ('header', 'text',)


@register(Comment)
class CommentTranslationOptions(TranslationOptions):
    fields = ('text',)
