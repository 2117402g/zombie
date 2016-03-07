from django.conf.urls import patterns, url
from zombie import views

urlpatterns = patterns('',
        url(r'^$', views.index, name='index'),
        url(r'^how_to_play/$', views.how_to_play, name='how_to_play'),
        url(r'^play/', views.play, name='play'),
        url(r'^leaderboards/', views.leaderboards, name='leaderboards'),
        url(r'^user/$', views.user, name='user'),
                       )