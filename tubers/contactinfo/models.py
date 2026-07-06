from django.db import models
from django.utils import timezone
from ckeditor.fields import RichTextField


class Contactinfo(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    fb_handle = models.CharField(max_length=255)
    insta_handle = models.CharField(max_length=255)
    youtube_handle = models.CharField(max_length=255)
    twitter_handle = models.CharField(max_length=255)
    description_1 = RichTextField(blank=True)
    description_2 = RichTextField(blank=True)
    phone = models.CharField(max_length=100)
    email = models.CharField(max_length=255)
    created_date = models.DateTimeField(blank=True, default=timezone.now)

    def __str__(self):
        return self.first_name
