import datetime

from django.db import models
from django.db.models.deletion import CASCADE
from django.utils import timezone
from django.contrib.auth.models import User
from django.core.validators import MinLengthValidator
import urllib.request, json
from operator import itemgetter

class Team(models.Model):
    name = models.TextField()
    abbreviation = models.TextField()
    color = models.CharField(max_length=6, validators=[MinLengthValidator(6)])
    altcolor = models.CharField(max_length=6, validators=[MinLengthValidator(6)])
    division = models.TextField()
    def __str__(self):
        return self.name

    def schedule(self):
        return Game.objects.filter(season=self.season).filter(home_team=self.Team) | Game.objects.filter(season=self.season).filter(away_team=self.Team)

class Game(models.Model):
    home_team = models.ForeignKey(Team, on_delete=CASCADE, related_name="home_team")
    away_team = models.ForeignKey(Team, on_delete=CASCADE, related_name="away_team")
    start_date = models.DateTimeField(null=True)
    home_score = models.PositiveIntegerField(default=0)
    away_score = models.PositiveIntegerField(default=0)
    finished = models.BooleanField(default=False)
    week = models.PositiveIntegerField(null=True)
    season = models.PositiveIntegerField(null=True)

    def spread(self):
        return self.home_score - self.away_score

    def __str__(self):
        return self.away_team.name + ' @ ' + self.home_team.name

    def winner(self):
        if self.home_score > self.away_score:
            return self.home_team
        elif self.home_score < self.away_score:
            return self.away_team
        else:
            return 'Tie'

    def isLive(self):
        return self.start_date <= timezone.now() and not self.finished

    def status(self):
        if self.finished:
            return "Final"
        elif self.isLive():
            return "Live"
        else:
            return "Not started"

    def update(self):
        if not self.finished:
            url = 'https://site.api.espn.com/apis/site/v2/sports/football/college-football/summary?event=' + str(self.id)
            with urllib.request.urlopen(url) as url:
                data = json.loads(url.read().decode())
                event = data['header']
                hscr = ascr = 0
                done = event['competitions'][0]['status']['type']['completed']
                pre = bool(event['competitions'][0]['status']['type']['state'] == 'pre')
                    
                for team in event['competitions'][0]['competitors']:
                    if team['homeAway'] == 'home':
                        if not pre:
                            hscr = int(team['score'])
                            home = team['team']['nickname']
                    else:
                        if not pre:
                            ascr = int(team['score'])
                            away = team['team']['nickname'] 
                self.home_score = hscr
                self.away_score = ascr
                self.start_date = event['competitions'][0]['date']
                self.finished = event['competitions'][0]['status']['type']['completed']
                self.save()

class League(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    points_spread = models.PositiveIntegerField(default=2)
    points_perfect = models.PositiveIntegerField(default=4)
    points_score = models.PositiveIntegerField(default=1)
    points_winner = models.PositiveIntegerField(default=4)
    name = models.TextField()
    season = models.PositiveIntegerField()
    team = models.ForeignKey(Team, on_delete=CASCADE)

    def createLeagueGames(self):
        for game in self.team.schedule:
            LeagueGame.objects.create(
                game = game,
                league = self
            )
    
    def __str__(self):
        return self.name + " " + str(self.season) + " (Owner: " + self.owner.username + ")"

    def updatePoints(self):
        for leagueGame in self.leaguegame_set.all():
            if not leagueGame.scored:
                leagueGame.assignPoints()
        return self

    def leaderboard(self):
        lb = []
        for userseason in self.userseason_set.all():
            lb.append([userseason.user.username, userseason.getGamePoints(), userseason.getBonusPoints(), userseason.getSchedulePoints(), userseason.getDivisionPoints(), userseason.getTotalPoints()])
        return sorted(lb, key=itemgetter(5), reverse=True)

    def completed(self):
        over = True
        for game in self.leaguegame_set.all():
            if not game.game.finished:
                over = False
        return over

    def uncwins(self):
        wins = 0
        for game in self.leaguegame_set.all():
            if game.game.winner() == 'North Carolina':
                wins += 1
        return wins
            
class UserSeason(models.Model):
    league = models.ForeignKey(League, on_delete=models.CASCADE)
    unc_wins = models.PositiveIntegerField(default=0)
    unc_losses = models.PositiveIntegerField(default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    unc_place = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.user.username + " (League: " + str(self.league) + ")"

    def getTotalPoints(self):
        return self.getGamePoints() + self.getBonusPoints() + self.getSchedulePoints() + self.getDivisionPoints()
        
    def getGamePoints(self):
        total = 0
        for pick in self.pick_set.all():
            total += pick.getTotalPoints()
        return total

    def getBonusPoints(self):
        total = 0
        for game in self.userbonusgamepick_set.all():
            if game.game.bonusgame.completed and game.pick == game.game.bonusgame.winner:
                total += self.league.points_bonus
        return total

    def getSchedulePoints(self):
        if self.league.completed and self.unc_wins == self.league.uncwins():
                return self.league.points_bonus
        return 0

    def getDivisionPoints(self):
        if self.league.completed and self.unc_place == self.league.unc_place:
                return self.league.points_bonus
        return 0

    def createPicks(self):
        for game in self.league.leaguegame_set.all():
            Pick.objects.create(
                leaguegame = game,
                userseason = self
            )

class LeagueGame(models.Model):
    league = models.ForeignKey(League, on_delete=models.CASCADE)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    scored = models.BooleanField(default=False)
    
    def __str__(self):
        return str(self.game) + " (League: " + str(self.league) +")"

    def assignPoints(self):
        if not self.scored and (self.game.finished or self.game.isLive()):
            if not self.game.finished:
                self.game.update()
            guess_winners, spread_winners, hscore_winners, ascore_winners, perfect_winners = ([] for i in range(5))
            best_spread = best_hscore = best_ascore = 0
            first = first_spread = True
            for pick in self.pick_set.all():
                pick.points_spread = 0
                pick.points_winner = 0
                pick.points_ascore = 0
                pick.points_hscore = 0
                pick.points_perfect = 0
                pick.save()
                if pick.isValid():
                    if pick.spread() * self.game.spread() > 0:
                        guess_winners.append(pick)
                        spread_difference = abs(pick.spread() - self.game.spread())
                        pick.points_winner = self.league.points_winner
                        if first_spread:
                            spread_winners = [pick]
                            best_spread = spread_difference
                            first_spread = False
                        elif spread_difference <= abs(best_spread):
                            if spread_difference < best_spread:
                                best_spread = spread_difference
                                spread_winners = []
                            spread_winners.append(pick) 
                    
                    home_difference = abs(pick.home_score - self.game.home_score)
                    away_difference = abs(pick.away_score - self.game.away_score)
                    if home_difference == 0 and away_difference == 0:
                        perfect_winners.append(pick)
                    if first:
                        best_hscore = home_difference
                        best_ascore = away_difference
                        hscore_winners.append(pick)
                        ascore_winners.append(pick)
                        first = False
                    else:
                        if home_difference <= best_hscore:
                            if home_difference < best_hscore:
                                best_hscore = home_difference
                                hscore_winners = []
                            hscore_winners.append(pick)
                        if away_difference <= best_ascore:
                            if away_difference < best_ascore:
                                best_ascore = away_difference
                                ascore_winners = []
                            ascore_winners.append(pick)
            for pick in spread_winners:
                pick.points_spread = self.league.points_spread
                pick.save()
            for pick in ascore_winners:
                pick.points_ascore = self.league.points_score
                pick.save()
            for pick in hscore_winners:
                pick.points_hscore = self.league.points_score
                pick.save()
            for pick in perfect_winners:
                pick.points_perfect = self.league.points_perfect
                pick.save()
            for pick in guess_winners:
                pick.points_winner = self.league.points_winner
                pick.save()
            if self.game.finished:
                self.scored = True
                self.save()
        elif not self.scored:
            self.game.update()
    
    def getLeaderboard(self):
        return sorted(self.pick_set.all(), key=lambda x: x.getTotalPoints(), reverse=True)

class Pick(models.Model):
    home_score = models.PositiveIntegerField(default=0)
    away_score = models.PositiveIntegerField(default=0)
    points_spread = models.PositiveIntegerField(default=0)
    points_perfect = models.PositiveIntegerField(default=0)
    points_ascore = models.PositiveIntegerField(default=0)
    points_hscore = models.PositiveIntegerField(default=0)
    points_winner = models.PositiveIntegerField(default=0)
    leaguegame = models.ForeignKey(LeagueGame, on_delete=models.CASCADE)
    userseason = models.ForeignKey(UserSeason, on_delete=models.CASCADE)

    def __str__(self):
        return self.userseason.user.username + ":" + str(self.leaguegame)

    def getTotalPoints(self):
        return self.points_spread + self.points_perfect + self.points_ascore + self.points_hscore + self.points_winner

    def spread(self):
        return self.home_score - self.away_score

    def isValid(self):
        return not (self.home_score == 0 and self.away_score == 0)
