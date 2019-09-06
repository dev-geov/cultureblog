from django.shortcuts import render
from django.views.generic import ListView, TemplateView
from django.views.generic.detail import DetailView
from django.db.models import Q
from .models import *


class AboutView(TemplateView):
    template_name = "blog/about.html"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Sobre"
        return context


class PostListView(ListView):
    #template_name = 'blog/post_list.html'
    model = Post
    object_list = None

    def get_queryset(self):
        search = self.request.GET.get('search', None)
        if search is not None:
            object_list = self.model.objects.filter(publish=True, slug__icontains=search)
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
        return context
