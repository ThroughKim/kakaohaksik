from django.contrib import admin
from .models import Log, Post

class LogAdmin(admin.ModelAdmin):
    list_display = ['id', 'success', 'timestamp']
admin.site.register(Log, LogAdmin)

class PostAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'link', 'timestamp']
admin.site.register(Post, PostAdmin)