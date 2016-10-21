from django.contrib import admin
from .models import Menu, Log

class MenuAdmin(admin.ModelAdmin):
    list_display = ['id', 'cafe_name', 'time', 'menu']

admin.site.register(Menu, MenuAdmin)

class LogAdmin(admin.ModelAdmin):
    list_display = ['id', 'cafe_name', 'timestamp']

admin.site.register(Log, LogAdmin)


