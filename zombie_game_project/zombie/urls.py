from django.conf.urls import patterns, url
from zombie import views

urlpatterns = patterns('',
        url(r'^$', views.index, name='index'),
        url(r'^how_to_play/$', views.how_to_play, name='how_to_play'),
        url(r'^leaderboards/', views.leaderboards, name='leaderboards'),
        url(r'^user/$', views.user, name='user'),
        url(r'^play/', views.play, name='play'),
        url(r'^login/',views.user_login, name = 'auth_login'),
        url(r'^register/$', views.register, name='register'),
        url(r'^turn/?P<action>[A-Z]+/(?P<num>[0-9]+)/$', views.turn, name='turn'),
        url(r'^logout/$', views.user_logout, name='auth_logout'),
                       )