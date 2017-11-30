from hc.api.models import Check
from hc.test import BaseTestCase


class AddCheckTestCase(BaseTestCase):
    def test_it_works(self):
        url = "/checks/add/"
        self.client.login(username="alice@example.org", password="password")
        r = self.client.post(url)
        self.assertRedirects(r, "/checks/")
        assert Check.objects.count() == 1

    def test_team_access_works(self):
        url = "/checks/add/"

        self.client.login(username="alice@example.org", password="password")
        resp = self.client.post(url)  # creates an unnamed check on the Alice profile
        self.assertRedirects(resp, "/checks/")
        alice_checks = Check.objects.filter(user=self.alice)
        self.client.logout()  # destroy the current session

        # Since Bob has team access, he should be able to access Alice's check
        # However this check is not Bobs so we can't access it
        # by querying Checks with user as Bob
        self.client.login(username="bob@example.org", password="password")

        resp = self.client.get("/checks/")
        self.assertContains(resp, alice_checks.first().code)  # UUID of alice's check present in the URL
        self.assertIn(str(alice_checks.first().code), str(resp.content))
        self.client.logout()

        # Since Charlie has no team access, on getting the `/checks/` page,
        # `You don't have any checks yet.` should be displayed
        self.client.login(username="charlie@example.org", password="password")
        resp = self.client.get("/checks/")
        self.assertContains(resp, "You don't have any checks yet.")
        self.client.logout()
