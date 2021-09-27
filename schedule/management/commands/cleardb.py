from django.core.management.base import BaseCommand, CommandError
from schedule.models import Game, League, UserSeason, LeagueGame, Pick
from django.contrib.auth.models import User 
import urllib.request, json, random

class Command(BaseCommand):
    help = 'Clears database'

    def handle(self, *args, **options):
        League.objects.all().delete()
        Game.objects.all().delete()
        