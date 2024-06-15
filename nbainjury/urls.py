from django.urls import path
from . import views

app_name = "nbainjury"
urlpatterns = [
    path("", views.index, name="index"),
    path("playerinfo", views.player_info, name="player-info"),
    path("<str:team_alias>/", views.team_injury_report, name="team_injury_report"),
    
]