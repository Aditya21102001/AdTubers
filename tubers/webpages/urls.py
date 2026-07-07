"""URL routes for the ``webpages`` app (mounted at the site root ``/``)."""

from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),              # /         → landing page
    path('about', views.about, name="about"),       # /about    → About Us
    path('services', views.services, name="services"),  # /services → Services
    path('contact', views.contact, name="contact"),     # /contact  → Contact
]
