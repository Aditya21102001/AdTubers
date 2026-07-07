"""Admin configuration for the ``hiretubers`` app.

Gives staff a booking inbox: filter/search requests, edit status inline, and
bulk-accept or bulk-decline via custom actions.
"""

from django.contrib import admin
from .models import Hiretuber


class HiretuberAdmin(admin.ModelAdmin):
    """Change-list configuration for booking requests."""

    list_display = ('id', 'first_name', 'email', 'tuber_name', 'status', 'created_date')
    list_display_links = ('id', 'first_name', 'email')
    list_editable = ('status',)  # change a booking's status without opening it
    search_fields = ('first_name', 'email', 'tuber_name')
    list_filter = ('status', 'city')
    actions = ('mark_accepted', 'mark_declined')

    @admin.action(description="Mark selected bookings as Accepted")
    def mark_accepted(self, request, queryset):
        # Bulk action: accept every selected booking in one query.
        queryset.update(status='accepted')

    @admin.action(description="Mark selected bookings as Declined")
    def mark_declined(self, request, queryset):
        # Bulk action: decline every selected booking in one query.
        queryset.update(status='declined')


admin.site.register(Hiretuber, HiretuberAdmin)
