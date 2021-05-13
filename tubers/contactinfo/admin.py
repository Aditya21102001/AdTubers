from django.contrib import admin
from .models import Contactinfo

# Register your models here.
class ContactinfoAdmin(admin.ModelAdmin):
    list_display = ('id','first_name', 'email', 'created_date')
    list_display_links = ('first_name', 'id')
    search_fields = ('first_name', 'email')
    list_filter = ('email', )

admin.site.register(Contactinfo, ContactinfoAdmin)
