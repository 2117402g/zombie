from django.shortcuts import render,render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login
from zombie.forms import UserForm, UserProfileForm


from zombie.models import UserProfile
from engine.game import Game

def index(request):
    context_dict = {}
    return render(request, 'zombie/index.html', context_dict)

def play(request):
    g = Game()
    g.start_new_day()
    print g.street.get_current_house()
    print g.street
    #if games exists
    # load game is it over?
    context_dict ={'player':g.player_state, 'game':g.game_state, 'turn_options': g.turn_options(),
                   'time_left':g.time_left, 'street': g.street , 'house_list': g.street.house_list,
                   'current_house': g.street.get_current_house(),
                   }
    return render(request,'zombie/play.html',context_dict)

#<li><a href="/scavenger/turn/{{turn}}/{{}}">{{ turn }}</a></li>
def turn(request,action,num):
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
    return render(request, 'zombie/play.html',context_dict)

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

def login(request):
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
    return render(request,
            'zombie/register.html',
            {'user_form': user_form, 'profile_form': profile_form, 'registered': registered} )