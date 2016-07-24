# coding: utf-8
from cStringIO import StringIO
import uuid
from django.core.files.base import ContentFile
from django.core.urlresolvers import reverse
from django.views.generic import TemplateView, ListView, CreateView, UpdateView, DetailView, FormView
from django.views.generic.edit import ModelFormMixin
from qiniu import put_file, etag
import qiniu
from flyingpang import settings
from flyingpang.dashboard.forms import CreateArticleForm, UpdateArticleForm, CreateTagForm, UpdateTagForm
from flyingpang.mysite.models import Article, Tag
from wand.image import Image
from flyingpang.myuser.models import MyUser


class ArticleListView(ListView):
    template_name = 'dashboard/mysite/article/list_article.html'

    def get_queryset(self):
        queryset = Article.objects.all()
        return queryset


class ArticleCreateView(CreateView):
    template_name = 'dashboard/mysite/article/create_article.html'
    form_class = CreateArticleForm

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.key = unicode(uuid.uuid4().get_hex())
        self.object.author = MyUser.objects.get(id=1)

        # handle uploaded image
        if self.request.FILES.get('photo'):
            uploaded_image = self.object.photo
            thumb_file = StringIO()

            with Image(file=uploaded_image.file) as original:
                original.resize(280, 180)
                with original.convert('jpeg') as img:
                    img.save(file=thumb_file)
            thumb_image = ContentFile(thumb_file.getvalue())
            self.object.photo.name = unicode(uuid.uuid4())[:8] + u'.jpg'
            self.object.photo.file = thumb_image

            # 将图片保存到本地的media中
            self.object.save()

            try:
                from flyingpang.settings import qiniu_access_key, qiniu_secret_key, bucket_name, qiniu_domain
                import qiniu

                if qiniu_access_key and qiniu_secret_key and bucket_name:
                    q = qiniu.Auth(qiniu_access_key, qiniu_secret_key)

                    # 上传本地文件

                    localfile = settings.BASE_DIR + self.object.photo.url
                    print localfile

                    key = self.object.photo.name[2:]  # 文件名
                    mime_type = 'image/jpeg'  # mimeType
                    params = {'x:a': 'a'}

                    token = q.upload_token(bucket_name, key)
                    ret, info = put_file(token, key, localfile, mime_type=mime_type, check_crc=True)
                    assert ret['key'] == key
                    assert ret['hash'] == etag(localfile)
                    self.object.img_url = "http://" + qiniu_domain + '/' + self.object.photo.name[2:]
                    self.object.save()

            except ImportError:
                pass

        self.object = form.save()
        return super(ModelFormMixin, self).form_valid(form)

    def get_success_url(self):
        return reverse('article_list_dashboard_view')


class ArticleUpdateView(UpdateView):
    template_name = 'dashboard/mysite/article/update_article.html'
    form_class = UpdateArticleForm
    model = Article

    def form_valid(self, form):
        self.object = form.save(commit=False)

        # handle uploaded image
        if self.request.FILES.get('photo'):
            uploaded_image = self.object.photo
            thumb_file = StringIO()

            with Image(file=uploaded_image.file) as original:
                original.resize(280, 180)
                with original.convert('jpeg') as img:
                    img.save(file=thumb_file)
            thumb_image = ContentFile(thumb_file.getvalue())
            self.object.photo.name = unicode(uuid.uuid4())[:8] + u'.jpg'
            self.object.photo.file = thumb_image

            # 将图片保存到本地的media中
            self.object.save()

            try:
                from flyingpang.settings import qiniu_access_key, qiniu_secret_key, bucket_name, qiniu_domain

                if qiniu_access_key and qiniu_secret_key and bucket_name:
                    q = qiniu.Auth(qiniu_access_key, qiniu_secret_key)

                    # 上传本地文件

                    localfile = settings.BASE_DIR + self.object.photo.url
                    print localfile

                    key = self.object.photo.name[2:]  # 文件名
                    mime_type = 'image/jpeg'  # mimeType
                    params = {'x:a': 'a'}

                    token = q.upload_token(bucket_name, key)
                    ret, info = put_file(token, key, localfile, mime_type=mime_type, check_crc=True)
                    assert ret['key'] == key
                    assert ret['hash'] == etag(localfile)
                    self.object.img_url = "http://" + qiniu_domain + "/" + self.object.photo.name[2:]

                    self.object.save()

            except ImportError:
                pass

        self.object = form.save()
        return super(ModelFormMixin, self).form_valid(form)

    def get_success_url(self):
        return reverse('article_list_dashboard_view')


class ArticlePreviewView(DetailView):
    template_name = 'dashboard/mysite/article/preview.html'
    model = Article


class TagListView(ListView):
    template_name = 'dashboard/mysite/tag/list_tag.html'

    def get_queryset(self):
        queryset = Tag.objects.all()
        return queryset


class TagCreateView(CreateView):
    template_name = 'dashboard/mysite/tag/create_tag.html'
    form_class = CreateTagForm

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.key = unicode(uuid.uuid4().get_hex())
        self.object = form.save()
        return super(ModelFormMixin, self).form_valid(form)

    def get_success_url(self):
        return reverse('tag_list_dashboard_view')


class TagUpdateView(UpdateView):
    template_name = 'dashboard/mysite/tag/update_tag.html'
    form_class = UpdateTagForm
    model = Tag

    def get_success_url(self):
        return reverse('tag_list_dashboard_view')
