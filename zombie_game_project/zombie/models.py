from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

class UserProfile(models.Model):
    # This line is required. Links UserProfile to a User model instance.
    user = models.OneToOneField(User, unique= True)

    # The additional attributes we wish to include.
    games_played = models.IntegerField(default=0)
    most_days_survived = models.IntegerField(default=0)
    most_kills = models.IntegerField(default=0)
    most_people = models.IntegerField(default=0)
    current_game = models.CharField(default= None, max_length=1024)
    picture = models.ImageField(upload_to='profile_images', blank=True)

    # Override the __unicode__() method to return out something meaningful!
    def __unicode__(self):
        return self.user.username

class Badge(models.Model):
    name = models.CharField(max_length=32, unique=True)
    desc = models.CharField(max_length=256, unique=True)
    Btype = models.CharField(max_length=8)
    criteria = models.IntegerField(default=0)
    level = models.IntegerField(default=0)
    icon = models.ImageField(upload_to='badge_icon', blank=True)

    def __unicode__(self):
        return self.name

class Achievement(models.Model):
    badge = models.ForeignKey(Badge)
    player = models.ForeignKey(UserProfile)
    date = models.DateTimeField()

    def __unicode__(self):
        return self.player.name