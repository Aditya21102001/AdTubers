"""Admin configuration for the ``youtubers`` app.

Registers :class:`~youtubers.models.Youtuber` with a customized change list so
staff can manage creators (with a thumbnail preview, search, and filters).
"""

from django.contrib import admin
from .models import Youtuber
from django.utils.html import format_html


class Ytadmin(admin.ModelAdmin):
    """Change-list configuration for the Youtuber model."""

    def myphoto(self, object):
        # Render the profile image as a small thumbnail in the list view.
        return format_html('<img src="{}" width="40" />'.format(object.photo.url))

    list_display = ('id', 'name', 'myphoto', 'subs_count', 'is_featured')
    search_fields = ('name', 'camera_type')
    list_filter = ('city', 'camera_type')
    list_display_links = ('id', 'name')
    list_editable = ('is_featured',)  # toggle "featured" straight from the list


admin.site.register(Youtuber, Ytadmin)
