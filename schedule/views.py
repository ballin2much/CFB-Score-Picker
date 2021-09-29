from datetime import date

from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from .forms import PickForm, LeagueForm

from .models import Game, LeagueGame, UserSeason, Pick, League

# Create your views here.
def index(request):
    if request.user.is_authenticated:
        return render(request, 'schedule/home.html', {'user': request.user, 'nav':'home'})
    else:
        return render(request, 'schedule/index.html', {'nav':'league'})

def schedule(request, year):
    games = Game.objects.filter(start_date__year = year).order_by('start_date')
    template = loader.get_template('schedule/index.html')
    context = {
        'games' : games,
    }
    return HttpResponse(template.render(context, request))

def submitpick(request, pickid):
    if request.method == 'POST':
        pick = Pick.objects.get(id=pickid)
        form = PickForm(request.POST, instance=pick)
        if form.is_valid():
            pick = form.save()
            return redirect(request.META.get('HTTP_REFERER', '/home'))
        else:
            return HttpResponse("This didn't work")

def createleague(request):
    if request.method == 'POST':
        form = LeagueForm(request.POST)
        if form.is_valid():
            league = form.save(commit = False)
            league.season = int(date.today().year)
            league.owner = request.user
            league.save()
            league.createLeagueGames()
            return HttpResponseRedirect('/league/'+str(league.id))
        else:
            return HttpResponse("This didn't work")
    else:
        form = LeagueForm()
        return render(request, 'schedule/createleague.html', {'form': form, 'nav':'create'})

def league(request, leagueid):
        if request.user.is_authenticated:
            if not UserSeason.objects.filter(league=leagueid, user=request.user).exists():
                l = UserSeason(
                    league = League.objects.get(id=leagueid),
                    user = request.user
                )
                l.save()
                l.createPicks()
            league = League.objects.get(id=leagueid).updatePoints()       
            season = UserSeason.objects.get(league=leagueid, user=request.user)
            form = PickForm()
            return render(request, 'schedule/league.html', {'season': season, 'form': form, 'league': league, 'nav': ''})
            
