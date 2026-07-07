"""Admin configuration for the ``contactinfo`` app.

Where staff edit the site's own contact details (kept as a single row that the
header/footer read on every page).
"""

from django.contrib import admin
from .models import Contactinfo


class ContactinfoAdmin(admin.ModelAdmin):
    """Change-list configuration for the site contact-info row."""

    list_display = ('id', 'first_name', 'email', 'created_date')
    list_display_links = ('first_name', 'id')
    search_fields = ('first_name', 'email')
    list_filter = ('email', )


admin.site.register(Contactinfo, ContactinfoAdmin)
