import os
import datetime
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'zombie_game_project.settings')

import django
django.setup()

from zombie.models import Achievement, Badge, UserProfile
from django.contrib.auth.models import User

def populate():

	#Add the 13 achievable badges to the game's database
	
	gold_survival = add_badge('Gold Survivor','survive for 15 days','most_days_survived','15','3','data/goldSurvival.png')
	silver_survival = add_badge('Silver Survivor','survive for 10 days','most_days_survived','10','2','data/silverSurvival.png')
	bronze_survival = add_badge('Bronze Survivor','survive for 5 days','most_days_survived','5','1','data/bronzeSurvival.png')
	
	gold_party = add_badge('Gold Partier','gain 15 party members','most_people','15','3','data/goldParty.png')
	silver_party = add_badge('Silver Partier','gain 10 party members','most_people','10','2','data/silverParty.png')
	bronze_party = add_badge('Bronze Partier','gain 5 party members','most_people','5','1','data/bronzeParty.png')
	
	gold_stamina = add_badge('Gold Stamina','play 15 games','games_played','15','3','data/goldStamina.png')
	silver_stamina = add_badge('Silver Stamina','play 10 games','games_played','10','2','data/silverStamina.png')
	bronze_stamina = add_badge('Bronze Stamina','play 5 games','games_played','5','1','data/bronzeStamina.png')
	
	gold_killer = add_badge('Gold Killer','kill 15 zombies','most_kills','15','3','data/goldKiller.png')
	silver_killer = add_badge('Silver Killer','kill 10 zombies','most_kills','10','2','data/silverKiller.png')
	bronze_killer = add_badge('Bronze Killer','kill 5 zombies','most_kills','5','1','data/bronzeKiller.png')
	
	platinum = add_badge('Pure Platinum','earn all other badges','badges','12','4','data/platinum.png')
	
	#Add ten users with random game statistics to the game's database
	
	kyle_user = add_user('Keyisle','Keyisle@gmail.com','password','15','5','10','5',None,'data/profile.png')
	leif_user = add_user('Leif','Leif@gmail.com','password','110', '290','230','60',None,'data/zombie.jpg')
	three_user = add_user('bob','bob@gmail.com','bob','0','0','0','0',None,'data/bird.png')
	four_user = add_user('jill','jill@gmail.com','jill','0','0','0','0',None,'data/penguin.png')
	five_user = add_user('jen','jen@gmail.com','jen','0','0','0','0',None,'data/mario.jpg')
	six_user = add_user('Gal','Gal@gmail.com','password','34','23','55','45',None,'data/person.png')
	seven_user = add_user('noob','noob@gmail.com','password','1','1','1','1',None,'data/noob.png')
	eight_user = add_user('robot','robot@gmail.com','password','101','11','100','1',None,'data/robot.png')
	nine_user = add_user('tom','tom@gmail.com','password','3','2','5','5',None,'data/dog.jpg')
	ten_user = add_user('wad2','wad2@gmail.com','password','340','223','155','451',None,'data/owl.png')
	
	#Add the appropriate achievements for one of the added users
	
	a1 = add_achievement(gold_stamina,kyle_user,date=datetime.datetime.now())
	a2 = add_achievement(silver_stamina,kyle_user,date=datetime.datetime.now())
	a3 = add_achievement(bronze_stamina,kyle_user,date=datetime.datetime.now())
	a4 = add_achievement(bronze_survival,kyle_user,date=datetime.datetime.now())	
	a5 = add_achievement(silver_killer,kyle_user,date=datetime.datetime.now())
	a6 = add_achievement(bronze_killer,kyle_user,date=datetime.datetime.now())
	a7 = add_achievement(bronze_party,kyle_user,date=datetime.datetime.now())	
	
	
#Adds a new type of badge to the database.	
def add_badge(name,desc,Btype,criteria,level,icon):
    b = Badge.objects.get_or_create(name=name)[0]
    b.desc=desc
    b.Btype=Btype
    b.criteria=criteria
    b.level=level
    b.icon=icon
    b.save()
    return b

#Adds a user to the database.
def add_user(usern,email,passw,games_played,most_days_survived,most_kills,most_people,current_game,picture):
    try:
		u = User.objects.get(username=usern)
		up = UserProfile(user=u)
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
    return up

#Adds an achievement to the database.
def add_achievement(badge,player,date):
    a = Achievement.objects.get_or_create(badge=badge,player=player)[0]
    a.date=date
    a.save()
    return a

# Start execution here!
if __name__ == '__main__':
    print "Starting zombie population script..."
    populate()
