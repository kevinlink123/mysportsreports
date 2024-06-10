from django.http import HttpResponse
from django.shortcuts import render
from django.conf import settings

from bs4 import BeautifulSoup
import requests
import os
import json


# Create your views here.

def index(request):
    context = {
        "title": "Home Page"
    }

    json_path = os.path.join(settings.BASE_DIR, "nbainjury", "static", "nbainjury", "data", "teams.json")
    with open(json_path, 'r') as json_file:
        context['teams_data'] = json.load(json_file)
    
    return render(request, "nbainjury/index.html", context)

def player_info(request):
    return HttpResponse("Some player info")

def team_injury_report(request, team_name):
    context = {
        "title": f"{team_name} Injury Report Info",
        "team_name": team_name,
    }
    return render(request, "nbainjury/team_injury_report.html", context)