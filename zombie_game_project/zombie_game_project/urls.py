from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
from registration.backends.simple.views import RegistrationView
from django.conf.urls.static import static

# Create a new class that redirects the user to the index page, if successful at logging

class MyRegistrationView(RegistrationView):
    def get_success_url(self, request):
        return '/accounts/register/complete/'

#The urls for the main app, the admin interface and django-registration-redux accounts
urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^scavenger/', include('zombie.urls')),
    url(r'^accounts/register/$', MyRegistrationView.as_view(), name='registration_register'),
    url(r'^accounts/', include('registration.backends.simple.urls')),
                       )



if settings.DEBUG:
    urlpatterns += patterns(
        'django.views.static',
        (r'^media/(?P<path>.*)',
        'serve',
        {'document_root': settings.MEDIA_ROOT}), )
if not settings.DEBUG:
        urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)



