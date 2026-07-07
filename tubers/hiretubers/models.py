"""Database model for the ``hiretubers`` app.

Defines :class:`Hiretuber` — one booking / "hire this creator" request submitted
from a creator's detail page. Admins review these and set the ``status``; a
logged-in user sees their own on the account dashboard.
"""

from django.db import models
from django.utils import timezone


class Hiretuber(models.Model):
    """A single booking request for a creator."""

    # Lifecycle of a booking, managed by staff in the admin.
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('declined', 'Declined'),
    )

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    tuber_id = models.IntegerField()               # id of the requested Youtuber (by value, not a FK)
    tuber_name = models.CharField(max_length=100)  # denormalized name, captured at request time
    city = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)
    email = models.CharField(max_length=255)
    state = models.CharField(max_length=100)
    message = models.TextField(blank=True)
    user_id = models.IntegerField(blank=True)      # requesting User's id, or "00" if anonymous
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_date = models.DateTimeField(blank=True, default=timezone.now)

    def __str__(self):
        return self.email
