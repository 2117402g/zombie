from django.shortcuts import render
from django.http import HttpResponse
from zombie.models import UserProfile
from engine.game import Game

def index(request):
    context_dict = {}
    return render(request, 'zombie/index.html', context_dict)

def play(request):
    g = Game()
    g.start_new_day()
    print g.game_state
    print g.player_state
    #if games exists
    # load game is it over?
    context_dict ={'player':g.player_state, 'game':g.game_state, 'turn_options': g.turn_options()}
    return render(request,'zombie/play.html',context_dict)

def leaderboards(request):
    mostDays = UserProfile.objects.order_by('-most_days_survived')[:20]
    mostKills = UserProfile.objects.order_by('-most_kills')[:20]
    mostPeople = UserProfile.objects.order_by('-most_people')[:20]
    context_dict = {'mostDays': mostDays,'mostKills':mostKills,'mostPeople':mostPeople}
    return render(request, 'zombie/leaderboards.html' , context_dict)

def user(request):
    return HttpResponse("user")

def how_to_play(request,):
    return HttpResponse("how_to_play")