from django.core.management.base import BaseCommand, CommandError
from schedule.models import League

class Command(BaseCommand):
    help = 'Updates league for any new games'

    def add_arguments(self, parser):
        parser.add_argument('year', type=int)

    def handle(self, *args, **options):
        for leaguetemp in League.objects.filter(season = options['year']):
            leaguetemp.createLeagueGames()
            for usertemp in leaguetemp.userseason_set.all():
                usertemp.createPicks()