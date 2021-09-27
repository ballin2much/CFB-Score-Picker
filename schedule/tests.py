from django.test import TestCase

# Create your tests here.
from .models import Game, League, UserSeason, LeagueGame, Pick
from django.contrib.auth.models import User

class TestModels(TestCase):
    
    def setUp(self):
        game = Game.objects.create(
            home_team="UNC",
            away_team="State",
            home_score=0,
            away_score=0,
            week=4,
            season=2018,
            finished=False,
            id=401013187
        )

        user1 = User.objects.create(username='user1', password='12345')
        user2 = User.objects.create(username='user2', password='12345') 
        user3 = User.objects.create(username='user3', password='12345') 

        league = League.objects.create(
            owner=user1,
            name="Test"        
        )

        leaguegame = LeagueGame.objects.create(
            league=league,
            game=game,
        )

        user1season = UserSeason.objects.create(
            league=league,
            user=user1
        )

        user2season = UserSeason.objects.create(
            league=league,
            user=user2
        )
        
        user3season = UserSeason.objects.create(
            league=league,
            user=user3
        )

        Pick.objects.create(
            userseason=user1season,
            home_score=29,
            away_score=35,
            leaguegame=leaguegame
        )

        Pick.objects.create(
            userseason=user2season,
            home_score=28,
            away_score=24,
            leaguegame=leaguegame
        )

        Pick.objects.create(
            userseason=user3season,
            home_score=28,
            away_score=34,
            leaguegame=leaguegame
        )

    def test_points(self):
        league = League.objects.get(name="Test").updatePoints()

        user1pick = Pick.objects.get(
            home_score=29, away_score=35
        )
            
        user2pick = Pick.objects.get(
            home_score=28, away_score=24
        )

        user3pick = Pick.objects.get(
            home_score=28, away_score=34
        )

        self.assertEqual(user1pick.getTotalPoints(), 6)
        self.assertEqual(user2pick.getTotalPoints(), 1)
        self.assertEqual(user3pick.getTotalPoints(), 12)
        self.assertEqual(Game.objects.get(id=401013187).finished, True)
        self.assertEqual(league.leaderboard(),[['user3', 12], ['user1', 6], ['user2', 1]])