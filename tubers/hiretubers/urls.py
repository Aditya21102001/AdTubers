"""URL routes for the ``hiretubers`` app (mounted at ``/hiretubers/``)."""

from django.urls import path
from . import views

urlpatterns = [
    path('hiretuber', views.hiretuber, name="hiretuber"),  # /hiretubers/hiretuber (POST target)
]
