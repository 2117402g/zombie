from django.shortcuts import render, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login
from zombie.forms import UserForm, UserProfileForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.template import RequestContext

import copy_reg
import types
from zombie.models import UserProfile, User, Achievement
from engine.game import Game
import pickle

def index(request):
    context_dict = {}
    return render(request, 'zombie/index.html', context_dict)

def fill_dict(g):

    if g.game_state == 'STREET':
        context_dict = {'player':g.player_state, 'game':g.game_state, 'turn_options': g.turn_options(),
                   'time_left':g.time_left,"move_options":[],'street': g.street , 'house_list': g.street.house_list,
                   'current_house': g.street.get_current_house(),'update_state':g.update_state,}
        i = 0
        for house in g.street.house_list:
            if house != g.street.get_current_house():
                context_dict["move_options"].append(i)
            i += 1
    elif g.game_state == 'HOUSE':
        context_dict = {'player':g.player_state, 'game':g.game_state, 'turn_options': g.turn_options(),
                   'time_left':g.time_left,"search_options":[],'current_house':g.street.get_current_house(),
                    'current_room':g.street.get_current_house().get_current_room(),'update_state':g.update_state,
                        'house':True,}
        #i= 0
        #for room in House(g).room_list:
         #  context_dict["search_options"].append(i)
          # i += 1
        #i=0
        #while i <= g.street.house_list.num_of_rooms:
         #   context_dict["search_options"].append(i)
          #  i+=1
    elif g.game_state == 'ZOMBIE':
        context_dict = {'num_zombies':g.street.get_current_house().get_current_room().zombies,
                        'player':g.player_state, 'game':g.game_state, 'turn_options': g.turn_options(),
                   'time_left':g.time_left,'update_state':g.update_state, }
    return context_dict

def _pickle_method(g):
    if g.im_self is None:
        return getattr, (g.im_class, g.im_func.func_name)
    else:
        return getattr, (g.im_self, g.im_func.func_name)

def _save(up,g):
    copy_reg.pickle(types.MethodType, _pickle_method)
    up.current_game = pickle.dumps(g)
    up.save()



@login_required
def play(request):
    up = UserProfile.objects.get(user= User.objects.get(username = request.user))
    if up.current_game != None:
        g = pickle.loads(up.current_game)
        if g.is_game_over():
            context_dict = {'game_over':True}
            return render(request,'zombie/play.html',context_dict)
        elif g.is_day_over():
            g.end_day()
            context_dict = {"end_of":g.player_state.days, 'player':g.player_state}
            g.start_new_day()
            _save(up,g)
            return render(request,'zombie/play.html',context_dict)
    else:
        g = Game()
        g.start_new_day()
    context_dict = fill_dict(g)
    _save(up,g)
    return render(request,'zombie/play.html',context_dict)

def turn(request,action,num):
    up = UserProfile.objects.get(user= User.objects.get(username = request.user))
    g = pickle.loads(up.current_game)
    action = str(action)
    if action in ['MOVE','SEARCH']:
        num = int(num)
        g.take_turn(action, num)
    else:
        g.take_turn(action)
    if g.is_game_over():
        context_dict = {'game_over':True}
        return render(request,'zombie/play.html',context_dict)
    elif g.is_day_over():
        g.end_day()
        context_dict = {"end_of":g.player_state.days, 'player':g.player_state}
        g.start_new_day()
        _save(up,g)
        return render(request,'zombie/play.html',context_dict)
    context_dict = fill_dict(g)
    _save(up,g)
    return render(request, 'zombie/play.html',context_dict)

def new_game(request):
    up = UserProfile.objects.get(user= User.objects.get(username = request.user))
    up.current_game = None
    up.save()
    return play(request)


def leaderboards(request):
    mostDays = UserProfile.objects.order_by('-most_days_survived')[:20]
    mostKills = UserProfile.objects.order_by('-most_kills')[:20]
    mostPeople = UserProfile.objects.order_by('-most_people')[:20]
    mostPlays = UserProfile.objects.order_by('-games_played')[:20]
    context_dict = {'mostPlays': mostPlays,'mostDays': mostDays, 'mostKills': mostKills, 'mostPeople': mostPeople}
    return render(request, 'zombie/leaderboards.html', context_dict)

def how_to_play(request ):
    return render(request,"zombie/how_to_play.html",{})


@login_required
def profile(request):
    context = RequestContext(request)
    context_dict = {}
    u = User.objects.get(username=request.user)
    try:
        up = UserProfile.objects.get(user=u)
    except:
        up = None
	
    try:
		a = Achievement.objects.filter(player=up)
    except:
		a = None
		print "fail"
		
    context_dict['user'] = u
    context_dict['userprofile'] = up
    context_dict['achievements'] = a
    return render_to_response('zombie/user.html', context_dict, context)