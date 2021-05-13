from django.contrib import admin
from .models import Contactpage


class ContactpageAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'email', 'created_date')
    list_display_links = ('first_name', 'id', 'email')
    search_fields = ('first_name', 'email')
    list_filter = ('email','city' )


    
admin.site.register(Contactpage, ContactpageAdmin)
