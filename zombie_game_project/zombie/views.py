from django.shortcuts import render
from django.http import HttpResponse
from zombie.models import UserProfile

def index(request):
    context_dict = {}
    return render(request, 'zombie/index.html', context_dict)

def play(request):
    return HttpResponse("play")

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