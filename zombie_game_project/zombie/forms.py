from django import forms
from django.contrib.auth.models import User
from zombie.models import UserProfile

#Form for changing a user profile's avatar.
class ImageForm(forms.ModelForm):
	class Meta:
		model = UserProfile
		fields = ('picture',)

