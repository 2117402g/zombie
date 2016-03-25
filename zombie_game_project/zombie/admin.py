from django.contrib import admin
from zombie.models import UserProfile ,Badge, Achievement

#Register the models used in the project.
admin.site.register(UserProfile)
admin.site.register(Badge)
admin.site.register(Achievement)

