from django.core.management.base import BaseCommand, CommandError
from schedule.models import Game, League, UserSeason, LeagueGame, Pick
from django.contrib.auth.models import User 
import urllib.request, json, random

class Command(BaseCommand):
    help = 'Creates some models for testing'

    def add_arguments(self, parser):
        parser.add_argument('name', type=str)

    def handle(self, *args, **options):
        League.objects.all().delete()

        user = User.objects.get(username="testuser")

        league = League.objects.create(
            owner=user,
            name=options['name']
        )

        userseason = UserSeason.objects.create(
            league=league,
            user=user
        )

        for game in Game.objects.filter(start_date__year = '2018'):
            temp = LeagueGame.objects.create(
                league = league,
                game = game
            )
            Pick.objects.create(
                leaguegame = temp,
                userseason=userseason,
                home_score=random.randint(0,60),
                away_score=random.randint(0,60)
            )

            temp.assignPoints()



        return "We made it."
