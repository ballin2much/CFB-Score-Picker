from django import forms
from .models import Pick, League, UserSeason
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
