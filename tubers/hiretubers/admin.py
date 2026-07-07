from django.contrib import admin
from .models import Hiretuber


class HiretuberAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'email', 'tuber_name', 'status', 'created_date')
    list_display_links = ('id', 'first_name', 'email')
    list_editable = ('status',)
    search_fields = ('first_name', 'email', 'tuber_name')
    list_filter = ('status', 'city')
    actions = ('mark_accepted', 'mark_declined')

    @admin.action(description="Mark selected bookings as Accepted")
    def mark_accepted(self, request, queryset):
        queryset.update(status='accepted')

    @admin.action(description="Mark selected bookings as Declined")
    def mark_declined(self, request, queryset):
        queryset.update(status='declined')


admin.site.register(Hiretuber, HiretuberAdmin)
