from django.http import HttpResponse
from django.shortcuts import render
from django.conf import settings

from datetime import datetime
from bs4 import BeautifulSoup, Comment
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

def team_injury_report(request, team_alias):
    json_path = os.path.join(settings.BASE_DIR, "nbainjury", "static", "nbainjury", "data", "team_aliases.json")
    team_name = ""
    with open(json_path, 'r') as json_file:
        team_name = json.load(json_file)[team_alias]

    now = datetime.now()
    current_year = now.year


    html_text = requests.get(f"https://www.basketball-reference.com/teams/{team_alias}/{current_year}.html").text
    soup = BeautifulSoup(html_text, 'lxml')

    all_injuries = soup.find(id="all_injuries")

    if not all_injuries:
        context = {
            "title": f"{team_alias} Injury Report Info",
            "team_name": team_name,
            "headers": [],
            "table_data": []
        }
        return render(request, "nbainjury/team_injury_report.html", context)

    comments = all_injuries.find_all(string=lambda text: isinstance(text, Comment))
    comment_soup = BeautifulSoup(comments[0], 'lxml')
    injury_table = comment_soup.find(id="div_injuries").find("table") if comment_soup.find(id="div_injuries").find("table") else "No injuries reported by the team!"

    table_data = []
    headers = [header.text for header in injury_table.find('thead').find_all('th')]
    for row in injury_table.find('tbody').find_all('tr'):
        player_name = row.find('th').text
        player_team = row.find('td', { "data-stat": "team_name" }).text
        player_last_report = row.find('td', { "data-stat": "note" }).text
        last_update = row.find('td', { "data-stat": "date_update" }).text
        
        player_info = {
            "name": player_name,
            "team": player_team,
            "last_report": player_last_report,
            "last_update": last_update
        }
        table_data.append(player_info)

    print(headers)

    context = {
        "title": f"{team_alias} Injury Report Info",
        "team_name": team_name,
        "headers": headers,
        "table_data": table_data
    }
    return render(request, "nbainjury/team_injury_report.html", context)

def player_info(request):
    return HttpResponse("Some player info")