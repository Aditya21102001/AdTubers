"""tubers URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf.urls.static import static
from django.conf import settings
from django.views.static import serve

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('webpages.urls')),
    path('youtubers/', include('youtubers.urls')),
    path('hiretubers/', include('hiretubers.urls')),
    path('contactpage/', include('contactpage.urls')),
    path('contactinfo/', include('contactinfo.urls')),
    path('accounts/', include('accounts.urls')),
    path('socialaccounts/', include('allauth.urls')),
    path('ckeditor5/', include('django_ckeditor_5.urls')),
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
