from django.core.management.base import BaseCommand, CommandError
from schedule.models import Game, Team
import urllib.request, json

class Command(BaseCommand):
    help = 'Pulls from ESPN API and fills teams'
    

    def handle(self, *args, **options):
        completeurl = "http://site.api.espn.com/apis/site/v2/sports/football/college-football/teams?limit=1000&groups=80"

        with urllib.request.urlopen(completeurl) as url:
            data = json.loads(url.read().decode())
            data = data['sports'][0]['leagues'][0]['teams']
            for team in data:
                team = team['team']
                if team.get('isActive',False):
                    Team.objects.create(
                        id = team['id'],
                        name = team['displayName'],
                        abbreviation = team['abbreviation'],
                        color = team.get('color',"FFFFFF"),
                        altcolor = team.get('altcolor',"FFFFFF"),
                        division = "FBS"
                    )

        completeurl = "http://site.api.espn.com/apis/site/v2/sports/football/college-football/teams?limit=1000&groups=81"

        with urllib.request.urlopen(completeurl) as url:
            data = json.loads(url.read().decode())
            data = data['sports'][0]['leagues'][0]['teams']
            for team in data:
                team = team['team']
                if team.get('isActive',False):
                    Team.objects.create(
                        id = team['id'],
                        name = team['displayName'],
                        abbreviation = team['abbreviation'],
                        color = team.get('color',"FFFFFF"),
                        altcolor = team.get('altcolor',"FFFFFF"),
                        division = "FCS"
                    )
