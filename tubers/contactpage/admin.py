"""Admin configuration for the ``contactpage`` app.

Lets staff read and search the messages left through the public contact form.
"""

from django.contrib import admin
from .models import Contactpage


class ContactpageAdmin(admin.ModelAdmin):
    """Change-list configuration for submitted contact messages."""

    list_display = ('id', 'first_name', 'email', 'created_date')
    list_display_links = ('first_name', 'id', 'email')
    search_fields = ('first_name', 'email')
    list_filter = ('email', 'city')


admin.site.register(Contactpage, ContactpageAdmin)
