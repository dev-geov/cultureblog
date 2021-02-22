from django.urls import path
from .views import *

app_name = 'blog'

urlpatterns = [
    path('', PostListView.as_view(), name="posts-index"),
    path('<slug:slug>/', PostDetailView.as_view(), name="post-detail"),
    path('<slug:slug>/new-comment', CreateCommentView.as_view(), name="comment-create"),
]
