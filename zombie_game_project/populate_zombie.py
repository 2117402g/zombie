import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'zombie_game_project.settings')

import django
django.setup()

from zombie.models import Achievement, Badge, UserProfile
from django.contrib.auth.models import User

def populate():
    kyle_user = add_user('Keyisle','Keyisle@gmail.com','password','21','73','64','99','','data/profile.png')
    leif_user = add_user('Leif','Leif@gmail.com','password','110', '290','230','60','','data/profile.png')
    three_user = add_user('Bob','Bob@gmail.com','password','51','4','23','6','','data/profile.png')
    four_user = add_user('Bill','Bill@gmail.com','password','31','88','45','62','','data/profile.png')
    five_user = add_user('Guy','Guy@gmail.com','password','11','48','25','62','','data/profile.png')
    six_user = add_user('Gal','Gal@gmail.com','password','34','23','55','45','','data/profile.png')
    seven_user = add_user('noob','noob@gmail.com','password','1','1','1','1','','data/profile.png')
    eight_user = add_user('robot','robot@gmail.com','password','101','11','100','1','','data/profile.png')
    nine_user = add_user('tom','tom@gmail.com','password','3','2','5','5','','data/profile.png')
    ten_user = add_user('wad2','wad2@gmail.com','password','340','223','155','451','','data/profile.png')
    
    gold_survival = add_badge('Gold Survivor','survive for 15 days','survival','15','3','data/goldSurvival.png')
	silver_survival = add_badge('Silver Survivor','survive for 10 days','survival','10','2','data/silverSurvival.png')
	bronze_survival = add_badge('Bronze Survivor','survive for 5 days','survival','5','1','data/bronzeSurvival.png')
	
	gold_party = add_badge('Gold Partier','gain 15 party members','party','15','3','data/goldParty.png')
	silver_party = add_badge('Silver Partier','gain 10 party members','party','10','2','data/silverParty.png')
	bronze_party = add_badge('Bronze Partier','gain 5 party members','party','5','1','data/bronzeParty.png')
	
	gold_stamina = add_badge('Gold Stamina','play 15 games','stamina','15','3','data/goldStamina.png')
	silver_stamina = add_badge('Silver Stamina','play 10 games','stamina','10','2','data/silverStamina.png')
	bronze_stamina add_badge('Bronze Stamina','play 5 games','stamina','5','1','data/bronzeStamina.png')
	
	gold_killer = add_badge('Gold Killer','kill 15 zombies','kills','15','3','data/goldKiller.png')
	silver_ killer = add_badge('Silver Killer','kill 10 zombies','kills','10','2','data/silverKiller.png')
	bronze_killer = add_badge('Bronze Killer','kill 5 zombies','kills','5','1','data/bronzeKiller.png')
	
def add_badge(name,desc,Btype,criteria,level,icon):
    b = Badge.objects.get_or_create(name=name)[0]
    b.desc=desc
    b.Btype=Btype
    b.criteria=criteria
    b.level=level
    b.icon=icon
    b.save()
    return b

def add_user(usern,email,passw,games_played,most_days_survived,most_kills,most_people,current_game,picture):
    try:
        u = User.objects.get(username=usern)
    except:
        u = User(username=usern, email=email)
        u.set_password(passw)
        u.save()
        up = UserProfile(user=u)
        up.games_played = games_played
        up.most_days_survived = most_days_survived
        up.most_kills = most_kills
        up.most_people = most_people
        up.current_game = current_game
        up.picture = picture
        up.save()

def add_achievement(badge,player,date):
    a = Achievement.objects.get_or_create(badge=badge,player=player)[0]
    a.date=date
    a.save()
    return a

# Start execution here!
if __name__ == '__main__':
    print "Starting Rango population script..."
    populate()
