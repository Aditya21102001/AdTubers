"""URL routes for the ``youtubers`` app (mounted at ``/youtubers/``)."""

from django.urls import path
from . import views

urlpatterns = [
    path('', views.youtubers, name="youtubers"),            # /youtubers/          → browse grid
    path('recommend', views.recommend, name="recommend"),   # /youtubers/recommend → AI match
    path('<int:id>', views.youtubers_detail, name="youtubers_detail"),  # /youtubers/5 → detail
    path('search', views.search, name="search"),            # /youtubers/search    → search results
]
