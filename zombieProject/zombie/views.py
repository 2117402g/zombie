from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    context_dict = {}
    return render(request, 'zombie/index.html', context_dict)

def play(request):
     return render(request, 'zombie/play.html', {})

def leaderboards(request):
     return render(request, 'zombie/leaderboards.html', {})

def user(request,):
     return render(request, 'zombie/user.html', {})

def how_to_play(request,):
     return render(request, 'zombie/how_to_play.html', {})