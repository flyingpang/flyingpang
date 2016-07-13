# coding: utf-8
from django.forms import ModelForm
from flyingpang.mysite.models import Article, Tag


class CreateArticleForm(ModelForm):

    class Meta:
        model = Article
        fields = ('title', 'summary', 'photo', 'tag', 'category', 'content', 'status')


class UpdateArticleForm(ModelForm):

    class Meta:
        model = Article
        fields = ('title', 'summary', 'photo', 'tag', 'category', 'content', 'status', 'is_removed')


class CreateTagForm(ModelForm):

    class Meta:
        model = Tag
        fields = ('name',)


class UpdateTagForm(ModelForm):

    class Meta:
        model = Tag
        fields = ('is_removed',)
