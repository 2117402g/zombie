from django.shortcuts import render, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.template import RequestContext

import datetime
import copy_reg
import types
from zombie.models import UserProfile, User, Achievement, Badge
from zombie.forms import ImageForm
from engine.game import Game
import pickle

#Index page view.
def index(request):
    context_dict = {}
    return render(request, 'zombie/index.html', context_dict)

#Allows the user to update their profile picture using the image form.
@login_required
def update_image(request):

	#Get current user profile
	up = UserProfile.objects.get(user=User.objects.get(username = request.user))
	
	#Is the request a post?
	if request.method == 'POST':
	
		#Initialise the image form
		image_form = ImageForm(request.POST, instance=up)
		
		#If the form is valid
		if image_form.is_valid():
		
			#Get the submitted image from the image form and save it to the user profile
			up.picture = request.FILES['picture']	
			up.save()
			return HttpResponseRedirect('/scavenger/user/')
	else:
		#If the request was not an HTTP post, display the form instead
		image_form = ImageForm(instance=up)
	return render(request,'zombie/update_image.html',{'image_form': image_form})

#A function which returns the game engine's current status.
def fill_dict(g):

	#Get the basic player data
    context_dict = {'party':g.player_state.party, 'ammo': g.player_state.ammo, 'kills': g.player_state.kills,
				   'days': g.player_state.days,'food': g.player_state.food}
				   
	#Is the player currently in a street?
    if g.game_state == 'STREET':
	
		#If so, get the relevant street data
        context_dict.update({'player':g.player_state.party, 'game':g.game_state, 'turn_options': g.turn_options(),
                   'time_left':g.time_left,"move_options":[],'street': g.street.name , 'house_list': g.street.house_list,
                   'stats': [], 'people': "x"*(min(g.player_state.party,30)), 'current_house': g.street.get_current_house()})
				   
        i = 0	
		#For each house in the street
        for house in g.street.house_list:
		
			#Add their relevant game data to a list 
				if context_dict['house_list'][i] == context_dict['current_house']:
					context_dict['location'] = i
				context_dict['stats'].append([house.num_of_rooms,house.get_house_stats()[3],i])
				context_dict["move_options"].append(i)
				i += 1
				
	#Is the player currently in a house?
    elif g.game_state == 'HOUSE':
	
		#If so, get the relevant house data
        context_dict.update({'player':g.player_state, 'game':g.game_state, 'turn_options': g.turn_options(),
                   'time_left':g.time_left,"search_options":[],'current_house':g.street.get_current_house(),
                    'current_room':g.street.get_current_house().get_current_room(),'update_state':g.update_state,
                        'house':True})
        
		#For each room in the house, add their relevant data to a list
        i= 0
        while i <= len(g.street.get_current_house().room_list):
           context_dict["search_options"].append(i)
           i += 1
		   
	#Is the player currently fighting a zombie?		   
    elif g.game_state == 'ZOMBIE':
		#If so, get the relevant fight data
        context_dict.update({'num_zombies':g.street.get_current_house().get_current_room().zombies,
                        'player':g.player_state, 'game':g.game_state, 'turn_options': g.turn_options(),
                   'time_left':g.time_left})
	
	#Return the relevant game statistics
    return context_dict

#Method for pickling the current game data.
def _pickle_method(g):
    if g.im_self is None:
        return getattr, (g.im_class, g.im_func.func_name)
    else:
        return getattr, (g.im_self, g.im_func.func_name)

#Save the current game data to the user profile, pickling it.
def _save(up,g):
    copy_reg.pickle(types.MethodType, _pickle_method)
    up.current_game = pickle.dumps(g)
    up.save()

#The view for when the player starts or resumes the game.
@login_required
def play(request):

	#Get the current user profile
    up = UserProfile.objects.get(user= User.objects.get(username = request.user))
	
	#If the user is resuming a game
    if up.current_game != None:
	
		#Load the pickled game data
        g = pickle.loads(up.current_game)
		
		#If the player has died
        if g.is_game_over():
		
			#Return the game over screen
            context_dict = {'game_over':True}
            return render(request,'zombie/play.html',context_dict)
		
		#Else if the in-game day is over
        elif g.is_day_over():
		
			#Return the day over screen and begin a new day, saving the game data
            g.end_day()
            context_dict = {"end_of":g.player_state.days, 'player':g.player_state}
            g.start_new_day()
            _save(up,g)
            return render(request,'zombie/play.html',context_dict)
			
	#If the player is starting a new game
    else:
		#Initialise a new game instance and start it
        g = Game()
        g.start_new_day()
		
	#Get the current game status, save the game data and return it
    context_dict = fill_dict(g)
    _save(up,g)
    return render(request,'zombie/play.html',context_dict)

#The view for when the player takes a turn in the game.	
def turn(request,action,num):
	
	#Get the current player
    up = UserProfile.objects.get(user= User.objects.get(username = request.user))
	
	#Get the current badges
    badges = Badge.objects.all()
	
	#Load the game data
    g = pickle.loads(up.current_game)
	
	#Get the user's action and take the turn
    action = str(action)
    if action in ['MOVE','SEARCH']:
        num = int(num)
        g.take_turn(action, num)
    else:
        g.take_turn(action)
		
	#Get the current game status
    context_dict = fill_dict(g)	
	
	#If the player died
    if g.is_game_over():
	
		#Return the game over screen
        context_dict = {'game_over':True}

		#For each existing badge
        for b in badges:
		
			#Check the user's games played
            if (b.Btype == 'games_played' and up.games_played >= b.criteria):
                 try:
					#Does the corresponding achievement already exist for that player?
                      a = Achievement.objects.get(badge=b,player=up)
                 except:
					#If not, create a new achievement for the player and save it
                      a = Achievement.objects.create(badge=b,player=up,date=datetime.datetime.now())
                      a.save()	
					  
        _save(up,g)
        return render(request,'zombie/play.html',context_dict)
		
	#Else if the in-game day is over
    elif g.is_day_over():
	
		#End the day
        g.end_day()
		
		#Update the player's records: do they have a new high-score in any category?
        up.most_kills = max(up.most_kills,context_dict['kills'])
        up.most_people = max(up.most_people,context_dict['party'])
        up.most_days_survived = max(up.most_days_survived,context_dict['days'])	
		
        context_dict = {"end_of":g.player_state.days, 'player':g.player_state, 'badges' : []}
		
		#For each existing badge
        for b in badges:
			#Compare the user's statistics against the badge criteria 
             if ((b.Btype == 'badges' and len(Achievement.objects.filter(player=up)) >= b.criteria) or (b.Btype == 'most_kills' and up.most_kills >= b.criteria) or (b.Btype == 'most_people' and up.most_people >= b.criteria) or (b.Btype == 'most_days_survived' and up.most_days_survived >= b.criteria)):
                 try:
					#Does the corresponding achievement already exist for that player?
                      a = Achievement.objects.get(badge=b,player=up)
                 except:
					#If not, create a new achievement for the player and save it
                      a = Achievement.objects.create(badge=b,player=up,date=datetime.datetime.now())
                      context_dict['badges'].append(b)
                      a.save()	

		#Start a new day, save the game data and return it.
        g.start_new_day()
        _save(up,g)
        return render(request,'zombie/play.html',context_dict)
	
	#Otherwise, simple save the game data and return the game status.
    _save(up,g)
    return render(request, 'zombie/play.html',context_dict)

#When the user requests to start a new game
def new_game(request):

	#Get the current user profile
    up = UserProfile.objects.get(user= User.objects.get(username = request.user))
    up.games_played = up.games_played + 1
	#Over-write the previous game data
    up.current_game = None
    up.save()
    return play(request)

#The data for the game's leaderboards
def leaderboards(request):

	#Return the top 20 players for each leaderboard category
    mostDays = UserProfile.objects.order_by('-most_days_survived')[:20]
    mostKills = UserProfile.objects.order_by('-most_kills')[:20]
    mostPeople = UserProfile.objects.order_by('-most_people')[:20]
    mostPlays = UserProfile.objects.order_by('-games_played')[:20]
    context_dict = {'mostPlays': mostPlays,'mostDays': mostDays, 'mostKills': mostKills, 'mostPeople': mostPeople}
    return render(request, 'zombie/leaderboards.html', context_dict)

#The how-to-play page
def how_to_play(request ):
    return render(request,"zombie/how_to_play.html",{})
	
#The user's personal profile page.
@login_required
def profile(request):
    context = RequestContext(request)
    context_dict = {}
	
	#Get the current user, their profile, and achievements.
    u = User.objects.get(username=request.user)
    try:
        up = UserProfile.objects.get(user=u)
    except:
        up = None
    try:
		a = Achievement.objects.filter(player=up)
    except:
		a = None
		
    context_dict['user'] = u
    context_dict['userprofile'] = up
    context_dict['achievements'] = a
    context_dict['no'] = len(a)*100
    return render_to_response('zombie/user.html', context_dict, context)