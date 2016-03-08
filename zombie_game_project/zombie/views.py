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
    print g.street.get_current_house()
    #if games exists
    # load game is it over?
    context_dict ={'player':g.player_state, 'game':g.game_state, 'turn_options': g.turn_options(),
                   'time_left':g.time_left, 'street': g.street , 'house_list': g.street.house_list,
                   'current_house': g.street.get_current_house(),
                   }
    return render(request,'zombie/play.html',context_dict)

def turn(action,num):
    g = Game()
    if action == ['MOVE','SEARCH']:
        g.take_turn(action, num)
    else:
        g.take_turn(action)
    if g.game_state == 'STREET':
        context_dict ={'player':g.player_state, 'game':g.game_state, 'turn_options': g.turn_options(),
                   'time_left':g.time_left, 'street': g.street , 'house_list': g.street.house_list,
                   'current_house': g.street.get_current_house(),
                   }
    elif g.game_state == 'HOUSE':
        context_dict = {'player':g.player_state, 'game':g.game_state, 'turn_options': g.turn_options(),
                    'time_left':g.time_left, 'current_house':g.street.get_current_house(),
                    'current_room':g.street.get_current_house().get_current_room()
        }
    elif g.game_state == 'ZOMBIE':
        context_dict = {'player':g.player_state, 'game':g.game_state, 'turn_options': g.turn_options(),
                    'time_left':g.time_left, 'num_zombies':g.street.get_current_house().get_current_room().zombies,
                        }
    return render('zombie/play.html',context_dict)

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