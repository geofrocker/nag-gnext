from hc.test import BaseTestCase
from hc.api.models import Check
from django.urls import reverse


class SwitchTeamTestCase(BaseTestCase):

    def setUp(self):
        super(SwitchTeamTestCase, self).setUp()
        self.url = reverse("hc-switch-team", args=(self.alice.username, ))

    def test_user_can_switch_team(self):
        """
            Test user can switch teams.

            Bob is a member of Alice's team,
            he is trying to swith to that team.
            Asserts that he is successfully redirected to hc-checks.
        """
        check = Check(user=self.alice, name="This belongs to Alice")
        check.save()

        self.client.login(username="bob@example.org", password="password")

        response = self.client.get(self.url, follow=True)

        # Todo Assert the contents of response
        self.assertRedirects(response, reverse("hc-checks"))

    def test_checks_team_membership(self):
        """
            Test switch team only works for users who are members for a team.

            Charlie is not a member of Alice's team but he is trying to switch to it.
            This asserts that an error code is returned.
        """
        self.client.login(username="charlie@example.org", password="password")

        response = self.client.get(self.url)
        # Todo Assert the expected error code
        self.assertEqual(response.status_code, 403)

    def test_user_can_switch_to_own_team(self):
        """
            Test that an owner of a team can successfully switch to that team.

            Alice owns a team, which she is trying to switch to.
            This asserts that no error code is returned to her.
        """
        self.client.login(username="alice@example.org", password="password")

        response = self.client.get(self.url, follow=True)

        # Todo Assert the expected error code
        self.assertNotEqual(response.status_code, 403)
