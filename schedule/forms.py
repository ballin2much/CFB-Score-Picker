from django import forms
from .models import Pick, League, UserSeason, UserBonusGamePick, LeagueBonusGame
from django.utils.translation import gettext_lazy as _

class PickForm(forms.ModelForm):
    class Meta:
        model = Pick
        fields = ['home_score', 'away_score']
        exclude = ['leaguegame', 'userseason', 'points_spread', 'points_perfect', 'points_ascore', 'points_hscore', 'points_winner']

class LeagueForm(forms.ModelForm):
    class Meta:
        model = League
        exclude = ['owner', 'season', 'unc_place']
        labels = {
            'name': _('League Name'),
        }

class UserSeasonForm(forms.ModelForm):
    class Meta:
        model = UserSeason
        exclude = ['league', 'points', 'user']
        labels = {
            'unc_wins': _('UNC Wins'),
            'unc_losses': _('UNC Losses'),
            'unc_place': _('ACC Coastal Placement')
        }

class UserBonusGamePickForm(forms.ModelForm):
    pick = forms.ChoiceField()

    def __init__(self, b, *args, **kwargs):
        super(UserBonusGamePickForm, self).__init__(*args, **kwargs)
        b2 = b.bonusgame
        self.fields['pick'].choices = [(b2.away_team, b2.away_team), (b2.home_team, b2.home_team)]
       

    class Meta:
        model = UserBonusGamePick
        exclude = ['userseason', "game"]
