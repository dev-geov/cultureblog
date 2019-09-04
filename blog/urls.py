from django.urls import path
from .views import *

urlpatterns = [
    path('', PostListView.as_view(), name="posts-index"),
    path('posts/<slug:slug>/', PostDetailView.as_view(), name="post-detail"),
    path('about/', AboutView.as_view(), name='about')
]
