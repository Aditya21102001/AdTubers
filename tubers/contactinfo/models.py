"""Database model for the ``contactinfo`` app.

Defines :class:`Contactinfo` — the site's *own* contact and social details.
Used as a single row (a singleton): most views load ``Contactinfo.objects.last()``
and pass it to the template so the shared header/footer can render the email,
phone, and social links.
"""

from django.db import models
from django.utils import timezone
from django_ckeditor_5.fields import CKEditor5Field


class Contactinfo(models.Model):
    """Site-wide contact details, edited by an admin (kept as a single row)."""

    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    fb_handle = models.CharField(max_length=255)       # social profile URLs / handles
    insta_handle = models.CharField(max_length=255)
    youtube_handle = models.CharField(max_length=255)
    twitter_handle = models.CharField(max_length=255)
    description_1 = CKEditor5Field(config_name='default', blank=True)  # rich-text "about" blocks
    description_2 = CKEditor5Field(config_name='default', blank=True)
    phone = models.CharField(max_length=100)
    email = models.CharField(max_length=255)
    created_date = models.DateTimeField(blank=True, default=timezone.now)

    def __str__(self):
        return self.first_name
