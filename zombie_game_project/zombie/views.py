from django.shortcuts import render, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login
from zombie.forms import UserForm, UserProfileForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.template import RequestContext

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
        print g.street.get_current_house()
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
        i=0
        while i <= g.street.house_list.num_of_rooms:
            context_dict["search_options"].append(i)
            i+=1
    elif g.game_state == 'ZOMBIE':
        context_dict = {'num_zombies':g.street.get_current_house().get_current_room().zombies,
                        'player':g.player_state, 'game':g.game_state, 'turn_options': g.turn_options(),
                   'time_left':g.time_left,'update_state':g.update_state, }
    return context_dict

def check(request,g):
    if g.is_day_over():
        g.end_day()
        g.start_new_day()
    if g.is_game_over():
        context_dict = {}
        return render(request, 'zombie/play.html',context_dict)

@login_required
def play(request):
    g = Game()
    g.start_new_day()
    up = UserProfile(user= User.objects.get(username = request.user))
    if up.current_game != "":
        cg = up.current_game
        # load up states
        # check if game is over
    else:
        g.start_new_day()
    context_dict = fill_dict(g)
    pps = pickle.dumps(g.player_state)
    pus = pickle.dumps(g.update_state)
    ps = pickle.dumps(g.street)
    pgs = pickle.dumps(g.game_state)
    up.current_game = "hi" #[pps,pus,ps,pgs]
    return render(request,'zombie/play.html',context_dict)

def turn(request,action,num):
    g = Game()
    action = str(action)
    if action in ['MOVE','SEARCH']:
        num = int(num)
        g.take_turn(action, num)
    else:
        g.take_turn(action)
    check(request,g)
    context_dict = fill_dict(g)
    return render(request, 'zombie/play.html',context_dict)


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