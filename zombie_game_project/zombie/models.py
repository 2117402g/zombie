from django.db import models
from django.contrib.auth.models import User
from registration.signals import *

#Model for the user's profile and their game statistics.
class UserProfile(models.Model):
    # This line is required. Links UserProfile to a User model instance.
    user = models.OneToOneField(User)

    # The user profile's game statistics and profile picture.
    games_played = models.IntegerField(default=0)
    most_days_survived = models.IntegerField(default=0)
    most_kills = models.IntegerField(default=0)
    most_people = models.IntegerField(default=0)
    current_game = models.CharField(max_length=20000,null=True)
    picture = models.FileField(upload_to='profile_images', default='data/profile.png')

    def __unicode__(self):
        return self.user.username

#Model for the badges that a player can earn while playing.
class Badge(models.Model):

	#The badges attributes and icon.
    name = models.CharField(max_length=32, unique=True)
    desc = models.CharField(max_length=256, unique=True)
    Btype = models.CharField(max_length=8)
    criteria = models.IntegerField(default=0)
    level = models.IntegerField(default=0)
    icon = models.ImageField(upload_to='badge_icon', blank=True)

    def __unicode__(self):
        return self.name

#Model for an achievement and the corresponding badge and player.
class Achievement(models.Model):

	#The badge and player are foreign keys of the achievement instance.
    badge = models.ForeignKey(Badge)
    player = models.ForeignKey(UserProfile)
    date = models.DateTimeField(null=True)
	
    def __unicode__(self):
        return self.player.user.username, self.badge

#Need to signal to create a UserProfile when registering a User
def createUserProfile(sender, user, request, **kwargs):
    UserProfile.objects.get_or_create(user=user)

user_registered.connect(createUserProfile)