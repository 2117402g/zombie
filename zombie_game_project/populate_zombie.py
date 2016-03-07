import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'djangoProject.settings')

import django
django.setup()

from zombie.models import Achievement, Badge, UserProfile


def populate():
    kyle_user = add_user('Keyisle','7','50','24','32','abcd','data/profile.png')
    kill_badge = add_badge('TestBadge','this is a test badge','kills','1','1','data/badge.png')

def add_badge(name,desc,Btype,criteria,level,icon):
    b = Badge.objects.get_or_create(name=name)[0]
    b.desc=desc
    b.Btype=Btype
	b.criteria=criteria
	b.level=level
	b.icon=icon
    b.save()
    return b

def add_user(user,games_played,most_days_survived,most_kills,most_people,current_game,picture):
    u = UserProfile.objects.get_or_create(user=user)[0]
    u.games_played = games_played
    u.most_days_survived = most_days_survived
	u.most_kills = most_kills
	u.most_people = most_people
	u.current_game = current_game
	u.picture = picture
    u.save()
    return u
	
def add_achievement(badge,player,date):
    a = Achievement.objects.get_or_create(badge=badge,player=player)[0]
    a.date=date
    a.save()
    return a

# Start execution here!
if __name__ == '__main__':
    print "Starting Rango population script..."
    populate()
