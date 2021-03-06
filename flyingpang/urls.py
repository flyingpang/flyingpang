"""flyingpang URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Import the include() function: from django.conf.urls import url, include
    3. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import url, include
from django.contrib import admin
from flyingpang.mysite.views import IndexView, ArticleDetailView, ArticleCategoryView, AboutMeView
from flyingpang.myuser.views import UserCreateView, LoginView, LogoutView

urlpatterns = [
    url(r'^admin/', admin.site.urls),

    url(r'^$', IndexView.as_view(), name='index_view'),
    url(r'^article/category/(?P<category>\w+)$', ArticleCategoryView.as_view(), name='article_category_view'),
    url(r'^article/detail/(?P<slug>\w+)/$', ArticleDetailView.as_view(), name='article_detail_view'),
    url(r'^about/$', AboutMeView.as_view(), name='about_me_view'),
    url(r'^register/$', UserCreateView.as_view(), name='user_create_view'),
    url(r'^login/$', LoginView.as_view(), name='login_view'),
    url(r'^logout/$', LogoutView.as_view(), name='logout_view'),

    # dashboard
    url(r'dashboard/', include('flyingpang.dashboard.urls')),
]

