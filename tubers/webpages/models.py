from django.db import models


class Team(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    role = models.CharField(max_length=255)
    fb_link = models.CharField(max_length=255, blank=True)
    insta_link = models.CharField(max_length=255, blank=True)
    photo = models.ImageField(upload_to='team/%Y/%m/%d/')
    youtube_link = models.CharField(max_length=255, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.first_name


class Slider(models.Model):
    headerline = models.CharField(max_length=255)
    subtitle = models.CharField(max_length=255)
    button_text = models.CharField(max_length=255)
    photo = models.ImageField(upload_to='slider/%Y/')
    created_date = models.DateTimeField(auto_now_add=True)
    link = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.headerline
