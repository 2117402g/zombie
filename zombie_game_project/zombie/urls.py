from django.conf.urls import patterns, url
from zombie import views

urlpatterns = patterns('',
        url(r'^$', views.index, name='index'),
        url(r'^how_to_play/$', views.how_to_play, name='how_to_play'),
        url(r'^leaderboards/', views.leaderboards, name='leaderboards'),
        url(r'^user/', views.profile, name='user'),
        url(r'^update_image/', views.update_image, name='update_image'),
        url(r'^play/', views.play, name='play'),
        url(r'^new_game/', views.new_game, name='new_game'),
        url(r'^turn/(?P<action>[A-Z]+)/(?P<num>[0-9]+)/', views.turn, name='turn')
                       )