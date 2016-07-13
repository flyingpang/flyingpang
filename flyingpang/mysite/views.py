# coding: utf-8
from django.core.cache import cache
from django.views.generic import TemplateView, DetailView, ListView
from flyingpang.local_settings import qiniu_domain
from flyingpang.mysite.models import Article


class IndexView(ListView):
    template_name = 'mysite/index.html'
    model = Article

    def get_queryset(self):
        queryset = Article.objects.filter(status=1, is_removed=0)
        return queryset

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['qiniu_domain'] = qiniu_domain
        popular_article_list = Article.objects.filter(status=1, is_removed=0).order_by('-zan_times', '-view_times')[:10]
        context['popular_article_list'] = popular_article_list
        return context


class ArticleCategoryView(ListView):
    template_name = 'mysite/list.html'

    def get_queryset(self):
        category = self.kwargs.get('category', None)
        queryset = Article.objects.filter(status=1, is_removed=0, category=category)
        return queryset

    def get_context_data(self, **kwargs):
        context = super(ArticleCategoryView, self).get_context_data(**kwargs)
        popular_article_list = Article.objects.filter(status=1, is_removed=0).order_by('-zan_times', '-view_times')[:10]
        context['popular_article_list'] = popular_article_list
        return context


class ArticleDetailView(DetailView):
    template_name = 'mysite/detail.html'
    model = Article

    def get(self, request, *args, **kwargs):
        try:
            article = Article.objects.get(slug=self.kwargs.get('slug', None))
            ip_address = self.request.META.get("REMOTE_ADDR", None)
            # if not cache.get("view_%(article_id)s_%(ip_address)s" % {"article_id": article.id, "ip_address": ip_address}):
                # cache.set("view_%(article_id)s_%(ip_address)s" % {"article_id": article.id, "ip_address": ip_address}, true)
        
            article.view_times += 1
            article.save()
        except Article.DoesNotExist:
            pass
        return super(ArticleDetailView, self).get(request, *args, **kwargs)


class AboutMeView(TemplateView):
    template_name = 'about.html'

    def get_context_data(self, **kwargs):
        context = super(AboutMeView, self).get_context_data(**kwargs)
        return context
