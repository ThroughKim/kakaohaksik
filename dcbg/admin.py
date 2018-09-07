from django.contrib import admin
from .models import Chat

class ChatAdmin(admin.ModelAdmin):
    list_display = ['id', 'sender', 'content', 'time']

admin.site.register(Chat, ChatAdmin)
