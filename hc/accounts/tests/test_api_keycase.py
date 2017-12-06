from django.core.urlresolvers import reverse
from hc.test import BaseTestCase

class ApiKeyCase(BaseTestCase):
    def setUp(self):
        super(ApiKeyCase, self).setUp()

        # login Charlie.
        self.client.login(username=self.charlie.email, password="password")

    # Test it creates and revokes API key
    def test_user_can_create_api(self):
        """
        Test user should be able to create and revoke API keys.
        """

        form = {'create_api_key': "1"}

        response = self.client.post(reverse('hc-profile'), form)

        # assert API key is created.
        self.assertIs(response.status_code, 200)
        self.assertContains(response, "The API key has been created!")

        self.charlie.profile.refresh_from_db()

        # API key now actually exists in Charlie profile.
        self.assertIsNot(self.charlie.profile.api_key, "")

    def test_user_can_revoke_api(self):
        # revoke API key.
        form = {'revoke_api_key': "1"}
        response = self.client.post(reverse('hc-profile'), form)

        self.charlie.profile.refresh_from_db()

        self.assertContains(response, 'The API key has been revoked!')

        # API key should be empty.
        self.assertEqual(self.charlie.profile.api_key, "")

"""
Completed. 

1. Email contents not checked.
2. Dry (self.client.login(username="alice@example.org", password="password").
3. Make a separate tests. (No need since it involves testing an inbuilt feature).
4. Separated tests create and revoke api key.
5. Fixed assert statement(assertTrue and assertEqual).
6. Assert contents of the response.
7. 

"""