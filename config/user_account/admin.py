from django.contrib import admin
from .models import UserAccount
# Register your models here.


class UserAccountAdmin(admin.ModelAdmin):
    list_filter = ('first_name', 'last_name' , 'username', 'email', 'is_private')
    search_fields = ('first_name', 'last_name' , 'username', 'email', 'is_private')
    list_display = ('first_name', 'last_name' , 'username', 'email', 'is_private')

admin.site.register(UserAccount, UserAccountAdmin)