from django.contrib import admin
from .models import Guest

@admin.register(Guest)
class GuestAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'number_of_companions')
