from django.core.management.base import BaseCommand, CommandError
from schedule.models import LeagueGame, UserSeason, League, Pick, Game
from django.contrib.auth.models import User
import urllib.request, random

class Command(BaseCommand):
    help = 'Fill DB with games'

    def handle(self, *args, **options):   
        League.objects.all().delete()
        league = League.objects.create(
            owner=User.objects.get(username="user1"),
            name="Test"        
        )

        user1season = UserSeason.objects.create(
            league=league,
            user=User.objects.get(username="user1")
        )

        user2season = UserSeason.objects.create(
            league=league,
            user=User.objects.get(username="user2")
        )
        
        user3season = UserSeason.objects.create(
            league=league,
            user=User.objects.get(username="user3")
        )

        for game in Game.objects.filter(season=2018):
            leaguegame = LeagueGame.objects.create(
                league=league,
                game=game,
                week=game.week
            )
            
            Pick.objects.create(
                userseason=user1season,
                home_score=random.randint(0,60),
                away_score=random.randint(0,60),
                game=leaguegame
            )

            Pick.objects.create(
                userseason=user2season,
                home_score=random.randint(0,60),
                away_score=random.randint(0,60),
                game=leaguegame
            )

            Pick.objects.create(
                userseason=user3season,
                home_score=random.randint(0,60),
                away_score=random.randint(0,60),
                game=leaguegame
            )




        


        