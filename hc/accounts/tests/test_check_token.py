from django.contrib.auth.hashers import make_password
from hc.test import BaseTestCase
from django.urls import reverse


class CheckTokenTestCase(BaseTestCase):

    def setUp(self):
        super(CheckTokenTestCase, self).setUp()
        self.profile.token = make_password("secret-token")
        self.profile.save()
        self.url = reverse('hc-check-token', args=('alice', 'secret-token'))

    def test_it_shows_form(self):
        r = self.client.get(self.url)
        self.assertContains(r, "You are about to log in")

    def test_it_redirects(self):
        r = self.client.post(self.url)
        self.assertRedirects(r, "/checks/")

        # After login, token should be blank
        self.profile.refresh_from_db()
        self.assertEqual(self.profile.token, "")

    ### Login and test it redirects already logged in
    def test_login_redirects_to_checks(self):
        # before login
        response = self.client.get(self.url)
        self.assertFalse(response.status_code == 302)
        self.assertTemplateUsed('accounts/check_token_submit.html')
        # after login
        self.client.post(self.url, follow=True)
        r = self.client.get(self.url)
        self.assertRedirects(r, reverse('hc-checks'))
        self.assertTrue(r.status_code == 302)

    ### Login with a bad token and check that it redirects
    def test_bad_token_redirects(self):
        r = self.client.post(reverse('hc-check-token', args=('alice', 'bad_token')), follow=True)
        self.assertRedirects(r, reverse('hc-login'))

    ### Any other tests?
