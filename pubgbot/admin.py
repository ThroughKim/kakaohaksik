from django.contrib import admin
from .models import Log, Users, SoloStats, DuoStats, SquadStats

class LogAdmin(admin.ModelAdmin):
    list_display = ['id', 'nickname', 'timestamp']

class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'user_name', 'timestamp', 'season']

class SoloAdmin(admin.ModelAdmin):
    list_display = ['id', 'user_name', 'timestamp', 'rounds_played', 'rating']

class DuoAdmin(admin.ModelAdmin):
    list_display = ['id', 'user_name', 'timestamp', 'rounds_played', 'rating']

class SquadAdmin(admin.ModelAdmin):
    list_display = ['id', 'user_name', 'timestamp', 'rounds_played', 'rating']

admin.site.register(Log, LogAdmin)
admin.site.register(Users, UserAdmin)
admin.site.register(SoloStats, SoloAdmin)
admin.site.register(DuoStats, DuoAdmin)
admin.site.register(SquadStats, SquadAdmin)