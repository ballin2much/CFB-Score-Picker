from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('schedule/<int:year>', views.schedule, name='scheduleyear'),
    path('submitpick/<pickid>', views.submitpick),
    path('league/create', views.createleague),
    path('league/<int:leagueid>', views.league)
]