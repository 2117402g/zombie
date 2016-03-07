from django import forms
from django.contrib.auth.models import User
from zombie.models import UserProfile


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password')

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('Games Played', 'Most Days Survived', 'Most kills' , 'Current Game','picture')
#'games_played','most_days_survived','most_kills','most_people','current_game',