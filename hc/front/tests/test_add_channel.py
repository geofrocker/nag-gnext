from django.test.utils import override_settings

from hc.api.models import Channel
from hc.test import BaseTestCase


@override_settings(PUSHOVER_API_TOKEN="token", PUSHOVER_SUBSCRIPTION_URL="url")
class AddChannelTestCase(BaseTestCase):

    def setUp(self):
        super(AddChannelTestCase, self).setUp()
        self.url = "/integrations/add/"
        self.client.login(username="alice@example.org", password="password")
        self.form = {"kind": "email", "value": "alice@example.org"}

    def test_it_adds_email(self):
        r = self.client.post(self.url, self.form)
        self.assertRedirects(r, "/integrations/")
        assert Channel.objects.count() == 1

    def test_it_trims_whitespace(self):
        """ Leading and trailing whitespace should get trimmed. """

        spaced_form = {"kind": "email", "value": "   alice@example.org   "}

        self.client.post(self.url, spaced_form)

        q = Channel.objects.filter(value="alice@example.org")
        self.assertEqual(q.count(), 1)

    def test_instructions_work(self):
        kinds = ("email", "webhook", "pd", "pushover", "hipchat", "victorops")
        for frag in kinds:
            url = "/integrations/add_%s/" % frag
            r = self.client.get(url)
            self.assertContains(r, "Integration Settings", status_code=200)

    def test_team_access(self):
        """ Tests if a check can be viewed by members on a
            team where by one member has team_access.
        """

        r = self.client.post(self.url, self.form)

        self.assertRedirects(r, "/integrations/")
        alice_channels = Channel.objects.filter(user=self.alice)
        self.client.logout()

        self.client.login(username="bob@example.org", password="password")

        resp = self.client.get("/integrations/")

        # UUID of alice's check present in the URL
        self.assertContains(resp, alice_channels.first().code)
        self.assertIn(str(alice_channels.first().code), str(resp.content))
        self.client.logout()

    def test_unknown_channels_cannot_work(self):
        bad_channel_form = {"kind": "WhatsApp", "value": "alice@example.org"}

        response = self.client.post(self.url, bad_channel_form)
        self.assertEqual(response.status_code, 400)

        url = '/integrations/add_whatsApp'
        resp = self.client.post(url)
        self.assertEqual(resp.status_code, 404)
