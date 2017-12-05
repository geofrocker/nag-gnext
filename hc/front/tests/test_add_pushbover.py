from django.test.utils import override_settings
from hc.api.models import Channel
from hc.test import BaseTestCase


@override_settings(PUSHOVER_API_TOKEN="token", PUSHOVER_SUBSCRIPTION_URL="url")
class AddPushoverTestCase(BaseTestCase):
    def setUp(self):
        super(AddPushoverTestCase, self).setUp()
        self.client.login(username="alice@example.org", password="password")
        session = self.client.session
        session["po_nonce"] = "n"
        session.save()

    def test_it_adds_channel(self):
        params = "pushover_user_key=a&nonce=n&prio=0"
        r = self.client.get("/integrations/add_pushover/?%s" % params)
        print(r.status_code)

        assert r.status_code == 302

        channels = list(Channel.objects.all())

        assert len(channels) == 1
        assert channels[0].value == "a|0"

    @override_settings(PUSHOVER_API_TOKEN=None)
    def test_it_requires_api_token(self):
        r = self.client.get("/integrations/add_pushover/")
        self.assertEqual(r.status_code, 404)

    def test_it_validates_nonce(self):
        params = "pushover_user_key=a&nonce=INVALID&prio=0"
        r = self.client.get("/integrations/add_pushover/?%s" % params)
        assert r.status_code == 403

    def test_pushover_validates_priority(self):
        """ A valid priority has a value between -2 and 2 both inclusive.
            using a value outside this range can indicate to us whether
            pushover validates priority or not.

            Priority 40 is non-existent so it is utilised here to show
            that invalid priorities don't work.
        """
        params = "pushover_user_key=a&nonce=n&prio=40"
        resp = self.client.get("/integrations/add_pushover/?%s" % params)
        self.assertEqual(resp.status_code, 400)
