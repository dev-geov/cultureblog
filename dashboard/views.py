from django.views.generic.list import ListView
from django.views.generic import FormView, RedirectView
from django.views.generic.detail import DetailView

from django.utils.http import is_safe_url
from django.contrib.auth import REDIRECT_FIELD_NAME, login as auth_login, logout as auth_logout
from django.contrib.auth.forms import AuthenticationForm
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters
from django.shortcuts import redirect


from blog.models import *


class LoginView(FormView):
    template_name = "dashboard/form_login.html"
    success_url = '/dashboard/'
    form_class = AuthenticationForm
    redirect_field_name = REDIRECT_FIELD_NAME

    @method_decorator(sensitive_post_parameters('password'))
    @method_decorator(csrf_protect)
    @method_decorator(never_cache)
    def dispatch(self, request, *args, **kwargs):
        request.session.set_test_cookie()
        return super(LoginView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        auth_login(self.request, form.get_user())

        if self.request.session.test_cookie_worked():
            self.request.session.delete_test_cookie()
        return super(LoginView, self).form_valid(form)

    def get_success_url(self):
        redirect_to = self.request.GET.get(self.redirect_field_name)
        if not is_safe_url(url=redirect_to, allowed_hosts=self.request.get_host()):
            redirect_to = self.success_url
        return redirect_to


class LogoutView(RedirectView):
    url = '/dashboard/login/'

    def get(self, request, *args, **kwargs):
        auth_logout(request)
        return super(LogoutView, self).get(request, *args, **kwargs)



class DashboardView(ListView):
    model = Post
    template_name = "dashboard/dashboard_list.html"
    title = "Login"

    def get(self, request, *args, **kwargs):
        if request.user.is_anonymous:
            return redirect('dashboard:login')
        return super(DashboardView, self).get(request, *args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Dashboard"
        user = BlogUser.objects.get(user=self.request.user)
        context["posts"] = Post.objects.filter(author=user)
        return context


class CategoryListView(ListView):
    template_name = 'dashboard/category_list.html'
    model = Category
    context_object_name = "categories"


    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Categorias"
        #context["categories"] = self.model.objects.all()
        return context


class PostDetailView(DetailView):
    model = Post
    template_name = "dashboard/post_detail.html"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = kwargs['object'].title
        return context


class CategoryDetailView(DetailView):
    model = Category
    template_name = "dashboard/category_detail.html"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = kwargs['object'].name
        context["posts"] = Post.objects.filter(category=kwargs['object'])
        return context
