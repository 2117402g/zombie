from django.shortcuts import render, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login
from zombie.forms import UserForm, UserProfileForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.template import RequestContext

from zombie.models import UserProfile
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
	
def play(request):
    g = Game()
    g.start_new_day()

    #if games exists
    # load game is it over?
    context_dict = fill_dict(g)
    pps = pickle.dumps(g.player_state)
    pus = pickle.dumps(g.update_state)
    ps = pickle.dumps(g.street)
    pgs = pickle.dumps(g.game_state)

    return render(request,'zombie/play.html',context_dict)

def turn(request,action,num):
    g = Game()
    action = str(action)
    if action in ['MOVE','SEARCH']:
        num = int(num)
        g.take_turn(action, num)
    else:
        g.take_turn(action)
    if g.is_day_over():
        g.end_day()
        g.start_new_day()
    if g.is_game_over():
        context_dict = {}
        return render(request, 'zombie/play.html',context_dict)
    context_dict = fill_dict(g)
    return render(request, 'zombie/play.html',context_dict)


def leaderboards(request):
	mostDays = UserProfile.objects.order_by('-most_days_survived')[:20]
	mostKills = UserProfile.objects.order_by('-most_kills')[:20]
	mostPeople = UserProfile.objects.order_by('-most_people')[:20]
	mostPlays = UserProfile.objects.order_by('-games_played')[:20]
	context_dict = {'mostPlays': mostPlays,'mostDays': mostDays, 'mostKills': mostKills, 'mostPeople': mostPeople}
	return render(request, 'zombie/leaderboards.html', context_dict)


def user(request):
    return render(request, "zombie/user.html", {})


def how_to_play(request ):
    return render(request,"zombie/how_to_play.html",{})


def user_login(request):
    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')

        # Use Django's machinery to attempt to see if the username/password
        # combination is valid - a User object is returned if it is.
        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/scavenger/')
            else:
                return HttpResponse("Your account is disabled.")
        else:
            print "Invalid login details: {0}, {1} ".format(username, password)
            context_dict = {'bad_details': "Invalid login details supplied."}
            return render_to_response('registration/login.html')

    else:
        return render(request, 'registration/login.html', {})


def register(request):
    registered = False

    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()

            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user

            # Did the user provide a profile picture?
            # If so, we need to get it from the input form and put it in the UserProfile model.
            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']

            # Now we save the UserProfile model instance.
            profile.save()

            # Update our variable to tell the template registration was successful.
            registered = True

        # Invalid form or forms - mistakes or something else?
        # Print problems to the terminal.
        # They'll also be shown to the user.
        else:
            print user_form.errors, profile_form.errors

    # Not a HTTP POST, so we render our form using two ModelForm instances.
    # These forms will be blank, ready for user input.
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    # Render the template depending on the context.
    return render(request,'registration/login.html',
                  {'user_form': user_form, 'profile_form': profile_form, 'registered':  registered})

@login_required
def user_logout(request):
    # Since we know the user is logged in, we can now just log them out.
    logout(request)

    # Take the user back to the homepage.
    return HttpResponseRedirect('/scavenger/')

@login_required
def profile(request):
    context = RequestContext(request)
    context_dict = {}
    u = User.objects.get(username=request.user)

    try:
        up = UserProfile.objects.get(user=u)
    except:
        up = None

    context_dict['user'] = u
    context_dict['userprofile'] = up
    return render_to_response('zombie/user.html', context_dict, context)