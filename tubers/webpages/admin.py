"""Admin configuration for the ``webpages`` app.

Registers :class:`~webpages.models.Team` and :class:`~webpages.models.Slider`,
each with a thumbnail preview in the change list.
"""

from django.contrib import admin
from .models import Slider, Team
from django.utils.html import format_html


class TeamAdmin(admin.ModelAdmin):
    """Change-list configuration for team members."""

    def myphoto(self, object):
        # Small thumbnail of the member's photo in the list view.
        return format_html('<img src="{}" width="40" />'.format(object.photo.url))
    list_display = ('id', 'myphoto', 'first_name', 'role', 'created_date')
    list_display_links = ('first_name', 'id')
    search_fields = ('first_name', 'role')
    list_filter = ('role', )


class SliderAdmin(admin.ModelAdmin):
    """Change-list configuration for homepage banner slides."""

    def myphoto(self, object):
        # Wider thumbnail since sliders are landscape banners.
        return format_html('<img src="{}" width="80" />'.format(object.photo.url))
    list_display = ('id', 'headerline', 'myphoto', 'subtitle', 'created_date')
    list_display_links = ('id', 'headerline')


admin.site.register(Slider, SliderAdmin)
admin.site.register(Team, TeamAdmin)
