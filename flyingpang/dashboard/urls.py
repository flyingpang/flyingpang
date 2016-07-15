# coding: utf-8
from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required
from flyingpang.dashboard.decorators import dashboard_admin_required
from flyingpang.dashboard.views import ArticleCreateView, ArticleUpdateView, ArticleListView, TagCreateView, TagListView, \
    TagUpdateView, ArticlePreviewView

urlpatterns = [
    # 测试使用,
    url(r'^$', login_required(ArticleListView.as_view()), name='article_list_dashboard_view'),
    url(r'article/$', dashboard_admin_required(ArticleListView.as_view()), name='article_list_dashboard_view'),
    url(r'article/create/$', dashboard_admin_required(ArticleCreateView.as_view()), name='article_create_dashboard_view'),
    url(r'article/(?P<pk>\d+)/update/$', dashboard_admin_required(ArticleUpdateView.as_view()), name='article_update_dashboard_view'),
    url(r'article/(?P<pk>\d+)/preview/$', dashboard_admin_required(ArticlePreviewView.as_view()), name='article_preview_dashboard_view'),

    # tag
    url(r'tag/list/$', dashboard_admin_required(TagListView.as_view()), name='tag_list_dashboard_view'),
    url(r'tag/create/$', dashboard_admin_required(TagCreateView.as_view()), name='tag_create_dashboard_view'),
    url(r'tag/(?P<pk>\d+)/update/$', dashboard_admin_required(TagUpdateView.as_view()), name='tag_update_dashboard_view'),
]
