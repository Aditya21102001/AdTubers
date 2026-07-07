"""URL routes for the ``contactinfo`` app (mounted at ``/contactinfo/``)."""

from django.urls import path
from . import views

urlpatterns = [
    path('', views.contactinfo, name="contactinfo"),  # /contactinfo/ (POST target)
]
