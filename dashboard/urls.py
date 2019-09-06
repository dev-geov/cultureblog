from django.urls import path, include
from dashboard.views import *

app_name = 'dashboard'
urlpatterns = [
    path('', DashboardView.as_view(), name="index"),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
]
