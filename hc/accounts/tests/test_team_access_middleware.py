from django.contrib.auth.models import User
from django.test import TestCase
from hc.accounts.models import Profile


class TeamAccessMiddlewareTestCase(TestCase):

    def test_it_handles_missing_profile(self):
        """
        Test user profile is created back if deleted or removed.
        """

        user = User(username="ned", email="ned@example.org")
        user.set_password("password")
        user.save()

        self.client.login(username="ned@example.org", password="password")
        r = self.client.get("/about/")
        self.assertEqual(r.status_code, 200)

        # Todo Assert the new Profile objects count
        # delete user profile instance.
        user.profile.delete()
        prev_count = Profile.objects.count()

        # make any request so that TeamAccessMiddleware
        # takes care of the missing profile.
        self.client.get("/about/")
        curr_count = Profile.objects.count()

        self.assertGreater(curr_count, prev_count)
