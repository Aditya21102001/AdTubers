"""Database models for the ``youtubers`` app.

Defines :class:`Youtuber` — one row per content creator listed in the
catalogue. These rows are created and edited by an admin through the Django
admin panel, and read on the public browse/search/detail/AI-match pages.
"""

from django.db import models
from django.utils import timezone
from django_ckeditor_5.fields import CKEditor5Field


class Youtuber(models.Model):
    """A single content creator (a "tuber") shown in the catalogue."""

    # Fixed option sets for the dropdown fields below. Each tuple is
    # (stored value, human label) — here they are intentionally identical.
    crew_choices = (
        ('solo', 'solo'),
        ('small', 'small'),
        ('large', 'large')
    )
    camera_choices = (
        ('canon', 'canon'),
        ('nikon', 'nikon'),
        ('sony', 'sony'),
        ('red', 'red'),
        ('fuji', 'fuji'),
        ('others', 'others')
    )
    category_choices = (
        ('code', 'code'),
        ('mobile_review', 'mobile_review'),
        ('vlog', 'vlog'),
        ('comedy', 'comedy'),
        ('gaming', 'gaming'),
        ('film_making', 'film_making'),
        ('cooking', 'cooking')
    )

    name = models.CharField(max_length=255)                 # creator / channel name
    price = models.IntegerField()                           # asking price to hire
    photo = models.ImageField(upload_to='ytubers/%Y/%m/')   # profile image (upload)
    video_url = models.CharField(max_length=255)            # YouTube video ID (embedded on detail page)
    description = CKEditor5Field(config_name='default')     # rich-text bio (HTML)
    city = models.CharField(max_length=255)                 # base city (used by the city filter)
    age = models.IntegerField()
    height = models.IntegerField()
    crew = models.CharField(choices=crew_choices, max_length=255)          # team size
    camera_type = models.CharField(choices=camera_choices, max_length=255)  # gear (used by the camera filter)
    subs_count = models.CharField(max_length=255)           # subscriber count, free text (e.g. "1.2M")
    category = models.CharField(choices=category_choices, max_length=255)   # content niche (used by the category filter)
    is_featured = models.BooleanField(default=False)        # if True, shown in the homepage "featured" row
    created_date = models.DateTimeField(default=timezone.now, blank=True)

    def __str__(self):
        # Shown in the admin list and dropdowns.
        return self.name
