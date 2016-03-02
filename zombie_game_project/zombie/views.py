from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    context_dict = {}
    return render(request, 'zombie/index.html', context_dict)

def play(request):
    return HttpResponse("play")

def leaderboards(request):
    return HttpResponse("leaderboards")

def user(request,):
    return HttpResponse("user")

def how_to_play(request,):
    return HttpResponse("how_to_play")