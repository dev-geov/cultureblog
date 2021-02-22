from django.shortcuts import render
from django.views.generic import ListView, TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView
from django.db.models import Q
from .models import *
from .forms import CommentForm
from django.shortcuts import redirect



class PostListView(ListView):
    #template_name = 'blog/post_list.html'
    model = Post
    object_list = None

    def get_queryset(self):
        search = self.request.GET.get('search', None)
        c = self.request.GET.get('category', None)

        if search is not None:
            object_list = self.model.objects.filter(publish=True, slug__icontains=search)
        elif c is not None:
            category = Category.objects.get(slug=c)
            object_list = self.model.objects.filter(publish=True, category=category)
        else:
            object_list = self.model.objects.filter(publish=True)
        return object_list


    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Posts"
        context["posts"] = self.object_list
        return context



class PostDetailView(DetailView):
    model = Post

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = kwargs['object'].title
        context["comment_form"] = CommentForm()
        context["comments"] = Comment.objects.filter(post=kwargs['object'])
        return context


class CreateCommentView(CreateView):
    model = Comment
    fields = ['email', 'content']
    success_url = None

    def post(self, request, *args, **kwargs):
        form = CommentForm(request.POST)

        if form.is_valid():
            post = Post.objects.get(slug=kwargs.get('slug'))
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect('blog:post-detail', post.slug)
