from django.contrib import admin
from .models import Hiretuber


class HiretuberAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'email', 'tuber_name', 'created_date')
    list_display_links = ('first_name', 'id', 'email')
    search_fields = ('first_name', 'email')
    list_filter = ('email','city' )


    
admin.site.register(Hiretuber, HiretuberAdmin)
