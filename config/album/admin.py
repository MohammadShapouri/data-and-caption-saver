from django.contrib import admin
from .models import Album
# Register your models here.


class AlbumAdmin(admin.ModelAdmin):
    list_filter = ('name', 'owner' , 'is_private')
    search_fields = ('name', 'owner' , 'is_private')
    list_display = ('name', 'owner' , 'is_private', 'creation_date', 'update_date')

admin.site.register(Album, AlbumAdmin)