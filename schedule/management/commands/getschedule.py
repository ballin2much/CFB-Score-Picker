from django.core.management.base import BaseCommand, CommandError
from schedule.models import Game, Team
import urllib.request, json

class Command(BaseCommand):
    help = 'Pulls from ESPN API and fills game'

    def add_arguments(self, parser):
        parser.add_argument('year', type=str)

    def handle(self, *args, **options):
        for teamtemp in Team.objects.filter(division="FBS"):
            url1 = "https://site.web.api.espn.com/apis/site/v2/sports/football/college-football/teams/"+ str(teamtemp.id) + "/schedule?region=us&lang=en&season="
            url2 = "&seasontype=2"
            completeurl = url1+options['year']+url2
            with urllib.request.urlopen(completeurl) as url:
                data = json.loads(url.read().decode())
                for event in data['events']:
                    home = away = ''
                    hscr = ascr = 0
                    done = event['competitions'][0]['status']['type']['completed']
                    pre = bool(event['competitions'][0]['status']['type']['state'] == 'pre')
                    for team in event['competitions'][0]['competitors']:
                        if team['homeAway'] == 'home':
                            if not pre:
                                hscr = team['score']['value']
                            home = Team.objects.get(id=team['team']['id'])
                        else:
                            if not pre:
                                ascr = team['score']['value']
                            away = Team.objects.get(id=team['team']['id'])
                    
                    if not Game.objects.get(id=event['id']).exists():
                        Game.objects.get_or_create(
                            home_team = home, 
                            away_team = away, 
                            start_date = event['date'], 
                            home_score = hscr, 
                            away_score = ascr, 
                            finished = done, 
                            week = event['week']['number'], 
                            season = options['year'],
                            id = event['id']
                        )
        return "We made it."
