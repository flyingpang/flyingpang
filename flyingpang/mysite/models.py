# coding: utf-8
from __future__ import unicode_literals

from django.db import models
from django.utils.text import slugify
from django.utils.translation import ugettext_lazy as _
from flyingpang import settings

CATEGORY_CHOICE = (
    ('read', _(u'读书')),
    ('code', _(u'编程')),
    ('invest', _(u'投资')),
    ('note', _(u'笔记')),
)


STATUS_CHOICE = (
    (0, _(u'草稿')),
    (1, _(u'正常')),
)


class Tag(models.Model):
    key = models.CharField(_(u'key'), max_length=32, unique=True)
    name = models.CharField(_(u'名称'), max_length=30, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(_(u'转义key'), max_length=60)
    is_removed = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.key)
        super(Tag, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.name


class Article(models.Model):
    key = models.CharField(_(u'key'), max_length=32, unique=True)
    title = models.CharField(_(u'标题'), max_length=60)
    summary = models.CharField(_(u'摘要'), max_length=200)
    photo = models.ImageField(_(u'本地图片'))
    img_url = models.URLField(_(u'七牛图片地址'), max_length=100, null=True)
    tag = models.ForeignKey(Tag, verbose_name=_(u'标签'))
    category = models.CharField(_(u'分类'), max_length=20, choices=CATEGORY_CHOICE)
    content = models.TextField(_(u'内容'))
    status = models.SmallIntegerField(_(u'状态'), choices=STATUS_CHOICE, default=0)
    slug = models.SlugField(_(u'转义key'), max_length=60)

    # Meta
    author = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_(u'作者'))
    created_at = models.DateTimeField(_(u'创建日期'), auto_now_add=True)
    updated_at = models.DateTimeField(_(u'更新日期'), auto_now_add=True)

    is_top = models.BooleanField(_(u'置顶'), default=False)
    view_times = models.IntegerField(_(u'浏览次数'), default=0)
    zan_times = models.IntegerField(_(u'赞次数'), default=0)
    is_removed = models.BooleanField(_(u'是否删除'), default=False)

    class Meta:
        ordering = ['-is_top', '-created_at']

    def save(self, *args, **kwargs):
        self.slug = slugify(self.key)
        super(Article, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.title
