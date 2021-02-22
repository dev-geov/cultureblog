from django.urls import path, include
from dashboard.views import *

app_name = 'dashboard'
urlpatterns = [
    path('', DashboardView.as_view(), name="index"),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('category/<slug:slug>/', CategoryDetailView.as_view(), name='category-detail'),
    path('post/<slug:slug>/', PostDetailView.as_view(), name='post-detail'),
    path('post-new/', PostCreateView.as_view(), name='post-new'),
    path('post-edit/<slug:slug>/', PostUpdateView.as_view(), name='post-edit'),
]
