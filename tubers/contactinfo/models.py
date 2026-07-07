from django.db import models
from django.utils import timezone
from django_ckeditor_5.fields import CKEditor5Field


class Contactinfo(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    fb_handle = models.CharField(max_length=255)
    insta_handle = models.CharField(max_length=255)
    youtube_handle = models.CharField(max_length=255)
    twitter_handle = models.CharField(max_length=255)
    description_1 = CKEditor5Field(config_name='default', blank=True)
    description_2 = CKEditor5Field(config_name='default', blank=True)
    phone = models.CharField(max_length=100)
    email = models.CharField(max_length=255)
    created_date = models.DateTimeField(blank=True, default=timezone.now)

    def __str__(self):
        return self.first_name
