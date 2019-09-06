from django.urls import path, include
from dashboard.views import *

app_name = 'dashboard'
urlpatterns = [
    path('', DashboardView.as_view(), name="index"),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('categories/', CategoryListView.as_view(), name='categories'),
    path('post/<slug:slug>/', PostDetailView.as_view(), name='post-detail'),
    path('category/<slug:slug>/', CategoryDetailView.as_view(), name='category-detail'),
]
