from hc.test import BaseTestCase
from hc.api.models import Check
from django.urls import reverse

class SwitchTeamTestCase(BaseTestCase):

    def setUp(self):
        super(SwitchTeamTestCase, self).setUp()
        self.url = reverse("hc-switch-team", args=(self.alice.username, ))

    def test_it_switches(self):
        c = Check(user=self.alice, name="This belongs to Alice")
        c.save()

        self.client.login(username="bob@example.org", password="password")

        r = self.client.get(self.url, follow=True)

        ### Assert the contents of r
        self.assertRedirects(r, reverse("hc-checks"))

    def test_it_checks_team_membership(self):
        self.client.login(username="charlie@example.org", password="password")

        r = self.client.get(self.url)
        ### Assert the expected error code
        assert r.status_code == 403

    def test_it_switches_to_own_team(self):
        self.client.login(username="alice@example.org", password="password")

        r = self.client.get(self.url, follow=True)
        
        ### Assert the expected error code
        assert r.status_code != 403