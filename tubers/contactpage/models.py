
from django.db import models
from datetime import datetime

# Create your models here.
class Contactpage(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100, blank=True)
    subject = models.TextField()
    city = models.CharField(max_length=100, blank=True)
    phone = models.CharField(max_length=100)
    email = models.CharField(max_length=255)
    state = models.CharField(max_length=100, blank=True)
    message = models.TextField(blank=True)
    created_date = models.DateTimeField(blank=True, default=datetime.now)

def __str__(self):
   return self.email 