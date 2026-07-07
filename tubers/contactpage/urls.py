"""URL routes for the ``contactpage`` app (mounted at ``/contactpage/``)."""

from django.urls import path
from . import views

urlpatterns = [
    path('', views.contactpage, name="contactpage"),  # /contactpage/ (POST target)
]
