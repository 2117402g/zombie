from django.conf.urls import patterns, url
from zombie import views

urlpatterns = patterns('',
        url(r'^$', views.index, name='index'),
        url(r'^how_to_play/$', views.how_to_play, name='how_to_play'),
        url(r'^leaderboards/', views.leaderboards, name='leaderboards'),
<<<<<<< HEAD
        url(r'^user/', views.profile, name='user'),
=======
        url(r'^user/$', views.profile, name='user'),
>>>>>>> f899f9f90a0c45e38f81511649014ec388ec3f6f
        url(r'^play/', views.play, name='play'),
        url(r'^turn/(?P<action>[A-Z]+)/(?P<num>[0-9]+)/', views.turn, name='turn')
                       )