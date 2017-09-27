from django.contrib import admin
from .models import Log, Users, SoloStats, DuoStats, SquadStats, ErrorUser

class LogAdmin(admin.ModelAdmin):
    list_display = ['id', 'nickname', 'timestamp']

class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'user_name', 'timestamp', 'season']

class SoloAdmin(admin.ModelAdmin):
    list_display = ['id', 'user_name', 'timestamp', 'rounds_played', 'rating', 'best_rank', 'win_ratio', 'top_10_ratio',
                    'kill_death_ratio', 'kills_pg', 'damage_pg', 'round_most_kills', 'percentile']

class DuoAdmin(admin.ModelAdmin):
    list_display = ['id', 'user_name', 'timestamp', 'rounds_played', 'rating', 'best_rank', 'win_ratio', 'top_10_ratio',
                    'kill_death_ratio', 'kills_pg', 'damage_pg', 'round_most_kills', 'percentile']

class SquadAdmin(admin.ModelAdmin):
    list_display = ['id', 'user_name', 'timestamp', 'rounds_played', 'rating', 'best_rank', 'win_ratio', 'top_10_ratio',
                    'kill_death_ratio', 'kills_pg', 'damage_pg', 'round_most_kills', 'percentile']

class ErrorAdmin(admin.ModelAdmin):
    list_display = ['id', 'user_name', 'timestamp']

admin.site.register(Log, LogAdmin)
admin.site.register(Users, UserAdmin)
admin.site.register(SoloStats, SoloAdmin)
admin.site.register(DuoStats, DuoAdmin)
admin.site.register(SquadStats, SquadAdmin)
admin.site.register(ErrorUser, ErrorAdmin)