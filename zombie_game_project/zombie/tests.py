from django.test import TestCase

from zombie.models import Badge, Achievement, User, UserProfile
from django.core.urlresolvers import reverse

class MethodTests(TestCase):

    def test_ensure_critera_is_positive(self):

        """
                ensure_critera_is_positive should results True for badge criteria where views are zero or positive
        """
        b = Badge(name='test',criteria=-1)
        b.save()
        self.assertEqual((b.criteria >= 0), True)

    def test_ensure_level_is_positive(self):

        """
                ensure_level_is_positive should results True for badge level where views are zero or positive
        """
        b = Badge(name='test',level=-1)
        b.save()
        self.assertEqual((b.level >= 0), True)

    def test_BType_length_limit(self):

        """
                BType_length_limit should ensure that an exception is thrown when a badge is created with BType length greater than eight
        """
        try:
			b = Badge(name='test',BType='this_is_too_long')
			b.save()
			self.assertEqual(1, 0)		
        except:
			pass
			
    def test_ensure_achievement_has_null_default_date(self):

        """
                ensure_achievement_has_null_default_date should results True when the default date for an achievement is null.
        """
        b = Badge(name='test')
        b.save()

        a = Achievement(badge=b)
        self.assertEqual(a.date, None)

class ViewTests(TestCase):

    def test_play_redirect(self):
        """
        Redirects to login screen when trying to play game.
        """
        response = self.client.get(reverse('play'))
        self.assertEqual(response.status_code, 302)	
		
    def test_user_redirect(self):
        """
        Redirects to login screen when trying to go to user page.
        """
        response = self.client.get(reverse('user'))
        self.assertEqual(response.status_code, 302)	

		
    def test_leaderboards(self):
        """
        Leaderboard contains the new user.
        """
        add_user('tester','t@t.com','t','567','0','0','0',None,'test.jpg')
		
        response = self.client.get(reverse('leaderboards'))
        self.assertEqual(response.status_code, 200)	
        self.assertContains(response, "tester")	
        self.assertContains(response, "567")		

#Adds a user to the database.
def add_user(usern,email,passw,games_played,most_days_survived,most_kills,most_people,current_game,picture):
    try:
		u = User.objects.get(username=usern)
		up = UserProfile(user=u)
    except:
        u = User(username=usern, email=email)
        u.set_password(passw)
        u.save()
        up = UserProfile(user=u)
        up.games_played = games_played
        up.most_days_survived = most_days_survived
        up.most_kills = most_kills
        up.most_people = most_people
        up.current_game = current_game
        up.picture = picture
        up.save()
    return up