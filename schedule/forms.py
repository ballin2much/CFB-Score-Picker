from django import forms
from .models import Pick, League, UserSeason, Team
from django.utils.translation import gettext_lazy as _

class PickForm(forms.ModelForm):
    class Meta:
        model = Pick
        fields = ['home_score', 'away_score']
        exclude = ['leaguegame', 'userseason', 'points_spread', 'points_perfect', 'points_ascore', 'points_hscore', 'points_winner']

class LeagueForm(forms.ModelForm):
    class Meta:
        model = League
        exclude = ['owner', 'season']
        labels = {
            'name': _('League Name'),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args,**kwargs)
        self.fields['team'].queryset = Team.objects.filter(division="FBS")