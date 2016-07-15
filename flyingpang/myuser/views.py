import urlparse
from django.contrib import auth
from django.contrib.auth import REDIRECT_FIELD_NAME, login
from django.contrib.auth.forms import AuthenticationForm
from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.generic import CreateView, FormView
from django.views.generic.base import TemplateResponseMixin, View
from flyingpang import settings
from flyingpang.myuser.forms import UserCreateForm
from flyingpang.myuser.models import MyUser
from flyingpang.myuser.utils import default_redirect


class UserCreateView(CreateView):
    template_name = 'myuser/register.html'
    form_class = UserCreateForm
    model = MyUser

    def form_valid(self, form):
        self.object = form.save(commit=False)
        return super(UserCreateView, self).form_valid(form)

    def get_success_url(self):
        return reverse('index_view')


class LoginView(FormView):
    template_name = 'myuser/login.html'
    form_class = AuthenticationForm
    redirect_field_name = REDIRECT_FIELD_NAME

    # @method_decorator(csrf_protect)
    # @method_decorator(never_cache)
    # def dispatch(self, request, *args, **kwargs):
    #     return super(LoginView, self).dispatch(self, request, *args, **kwargs)

    def form_valid(self, form):
        login(self.request, form.get_user())
        return super(LoginView, self).form_valid(form)

    def get_success_url(self):
        next = self.request.GET.get('next', None)
        if next:
            return next

        redirect_to = self.request.GET.get('next', None)
        if not redirect_to:
            redirect_to = '/'
        else:
            netloc = urlparse.urlparse(redirect_to)[1]
            # Security check -- don't allow redirection to a different host.
            if netloc and netloc != self.request.get_host():
                redirect_to = '/'

        return redirect_to


class LogoutView(TemplateResponseMixin, View):
    template_name = 'myuser/logout.html'
    redirect_field_name = 'next'

    def get(self, *args, **kwargs):
        if not self.request.user.is_authenticated():
            return redirect(self.get_redirect_url())
        context = self.get_context_data()
        return self.render_to_response(context)

    def post(self, *args, **kwargs):
        if self.request.user.is_authenticated():
            auth.logout(self.request)
        return redirect(self.get_redirect_url())

    def get_context_data(self, **kwargs):
        context = kwargs
        redirect_field_name = self.get_redirect_field_name()
        context.update({
            'redirect_field_name': redirect_field_name
        })
        return context

    def get_redirect_field_name(self):
        return self.redirect_field_name

    def get_redirect_url(self, fallback_url=None, **kwargs):
        if fallback_url is None:
            fallback_url = settings.LOGIN_URL
        kwargs.setdefault("redirect_field_name", self.get_redirect_field_name())
        return default_redirect(self.request, fallback_url, **kwargs)
