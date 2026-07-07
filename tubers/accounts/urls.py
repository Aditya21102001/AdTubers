"""URL routes for the ``accounts`` app (mounted at ``/accounts/``)."""

from django.urls import path
from . import views

urlpatterns = [
    path('login', views.login, name="login"),            # /accounts/login
    path('logout', views.logout_user, name="logout"),    # /accounts/logout
    path('register', views.register, name="register"),   # /accounts/register
    path('dashboard', views.dashboard, name="dashboard"),  # /accounts/dashboard (login required)
]
