from django.views.generic.list import ListView
from django.views.generic import FormView, RedirectView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, FormView, UpdateView

from django.utils.http import is_safe_url
from django.contrib.auth import REDIRECT_FIELD_NAME, login as auth_login, logout as auth_logout
from django.contrib.auth.forms import AuthenticationForm
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters
from django.shortcuts import redirect


from blog.models import *
from .forms import PostForm, ContactForm


class ContactView(FormView):
    template_name = "blog/contact.html"
    form_class = ContactForm
    success_url = 'contact'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Contatos"
        context["form"] = ContactForm()
        return context
    
    def form_valid(self, form):
        form.send_email()
        return super().form_valid(form)


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
        context["categories"] = Category.objects.all()
        if self.request.GET.get('filter'):
            filter = self.request.GET.get('filter')
            if filter == 'published':
                context["posts"] = Post.objects.filter(
                    author__user=self.request.user,
                    publish=True,
                )
            elif filter == 'unpublished':
                context["posts"] = Post.objects.filter(
                    author__user=self.request.user,
                    publish=False,
                )
        else:
            context["posts"] = Post.objects.filter(
                author__user=self.request.user,
            )
        return context


class PostDetailView(DetailView):
    model = Post
    template_name = "dashboard/post_detail.html"
    form_class = PostForm

    def get(self, request, *args, **kwargs):
        if request.user.is_anonymous:
            return redirect('dashboard:login')
        return super(PostDetailView, self).get(request, *args, **kwargs)

    def get_context_data(self, *args, **kwargs):

        post = kwargs['object']
        context = super().get_context_data(**kwargs)
        context["title"] = post.title
        context["post"] = post
        return context


class PostCreateView(CreateView):
    model = Post
    template_name = "dashboard/post_form.html"
    fields = ['title', 'content', 'publish', 'category']
    success_url = "blog:posts"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Novo post"
        return context
    
    def get(self, request, *args, **kwargs):
        if request.user.is_anonymous:
            return redirect('dashboard:login')
        return super(PostCreateView, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        form = PostForm(request.POST)

        if form.is_valid():
            post = form.save(commit=False)
            blog_user = BlogUser.objects.get(user=request.user)
            post.author = blog_user
            post.save()
            form.save_m2m()
            return redirect('dashboard:index')


class PostUpdateView(UpdateView):
    model = Post
    fields = fields = ['title','content','publish', 'category']
    template_name = "dashboard/post_form.html"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = f"Editar post: {self.object.title}"
        return context
    
    def post(self, request, *args, **kwargs):
        post = Post.objects.get(slug=kwargs.get('slug'))
        form = PostForm(request.POST, instance=post)

        if form.is_valid():
            post = form.save()
            return redirect('dashboard:post-detail', post.slug)


class CategoryDetailView(DetailView):
    model = Category
    template_name = "dashboard/category_detail.html"

    def get(self, request, *args, **kwargs):
        if request.user.is_anonymous:
            return redirect('dashboard:login')
        return super(CategoryDetailView, self).get(request, *args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = kwargs['object'].name
        context["categories"] = Category.objects.all()
        context["posts"] = Post.objects.filter(category=kwargs['object'])
        return context
