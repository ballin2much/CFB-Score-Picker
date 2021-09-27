from django.contrib import admin

# Register your models here.
from django.contrib.auth.models import User
from .models import Game, League, UserSeason, LeagueGame, Pick, BonusGame, LeagueBonusGame, UserBonusGamePick

admin.site.register(Game)
admin.site.register(League)
admin.site.register(UserSeason)
admin.site.register(LeagueGame)
admin.site.register(Pick)
admin.site.register(BonusGame)
admin.site.register(LeagueBonusGame)
admin.site.register(UserBonusGamePick)