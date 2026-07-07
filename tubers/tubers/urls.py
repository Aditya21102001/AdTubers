"""Root URL configuration for the tubers project.

This is the top-level router: it wires the admin, third-party apps, and each of
the six custom apps onto a URL prefix, then delegates to that app's own
``urls.py``. See https://docs.djangoproject.com/en/5.2/topics/http/urls/.
"""
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf.urls.static import static
from django.conf import settings
from django.views.static import serve

urlpatterns = [
    path('admin/', admin.site.urls),                        # Django admin panel
    path('', include('webpages.urls')),                     # home, about, services, contact
    path('youtubers/', include('youtubers.urls')),          # creator catalogue + AI match
    path('hiretubers/', include('hiretubers.urls')),        # booking-request form handler
    path('contactpage/', include('contactpage.urls')),      # public contact-form handler
    path('contactinfo/', include('contactinfo.urls')),      # site contact-info form handler
    path('accounts/', include('accounts.urls')),            # login / register / dashboard
    path('socialaccounts/', include('allauth.urls')),       # allauth (Google/Facebook login)
    path('ckeditor5/', include('django_ckeditor_5.urls')),  # rich-text editor endpoints
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
else:
    # Serve the committed demo media in production too (single-process friendly).
    # NOTE: uploads to the local filesystem are ephemeral on most hosts — for
    # durable user uploads switch to object storage (S3 / Cloudflare R2) via
    # django-storages.
    urlpatterns += [
        re_path(
            r'^media/(?P<path>.*)$',
            serve,
            {'document_root': settings.MEDIA_ROOT},
        ),
    ]
