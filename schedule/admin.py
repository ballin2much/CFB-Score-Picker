from django.contrib import admin

# Register your models here.
from django.contrib.auth.models import User
from .models import Game, League, UserSeason, LeagueGame, Pick, Team

admin.site.register(Game)
admin.site.register(League)
admin.site.register(UserSeason)
admin.site.register(LeagueGame)
admin.site.register(Pick)
class TeamAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)
admin.site.register(Team, TeamAdmin)