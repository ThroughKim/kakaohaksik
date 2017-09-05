from django.contrib import admin
from .models import Log

class LogAdmin(admin.ModelAdmin):
    list_display = ['id', 'nickname', 'timestamp']

admin.site.register(Log, LogAdmin)