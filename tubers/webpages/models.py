"""Database models for the ``webpages`` app.

Holds the two pieces of admin-managed content that the marketing pages render:

* :class:`Team`   — an "About us" team member.
* :class:`Slider` — a banner slide in the homepage carousel.
"""

from django.db import models


class Team(models.Model):
    """One team member shown on the Home and About pages."""

    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    role = models.CharField(max_length=255)                  # e.g. "Founder & CEO"
    fb_link = models.CharField(max_length=255, blank=True)   # optional social links
    insta_link = models.CharField(max_length=255, blank=True)
    photo = models.ImageField(upload_to='team/%Y/%m/%d/')
    youtube_link = models.CharField(max_length=255, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)   # set once, on creation

    def __str__(self):
        return self.first_name


class Slider(models.Model):
    """One banner slide in the homepage carousel."""

    headerline = models.CharField(max_length=255)   # big headline text
    subtitle = models.CharField(max_length=255)     # supporting line under it
    button_text = models.CharField(max_length=255)  # call-to-action label
    photo = models.ImageField(upload_to='slider/%Y/')
    created_date = models.DateTimeField(auto_now_add=True)
    link = models.CharField(max_length=255, blank=True)  # where the button points

    def __str__(self):
        return self.headerline
