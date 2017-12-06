from django.contrib.auth.hashers import make_password
from hc.test import BaseTestCase
from django.urls import reverse


class CheckTokenTestCase(BaseTestCase):

    def setUp(self):
        super(CheckTokenTestCase, self).setUp()
        self.profile.token = make_password("secret-token")
        self.profile.save()
        self.url = reverse('hc-check-token', args=('alice', 'secret-token'))

    def test_shows_form_with_get(self):
        """
            Test returns form with GET method.

            With GET method, a HTML form is returned.
            Asserts that the response contains text from HTML form.
        """
        response = self.client.get(self.url)
        self.assertContains(response, "You are about to log in")

    def test_redirect_with_post(self):
        """
            Test redirects with POST method.

            With post method, a user with the correct cretentials is logged.
            asserts that the user is redirected to checks.
            asserts that the token is destroyed after login.
        """
        response = self.client.post(self.url)
        self.assertRedirects(response, "/checks/")

        # After login, token should be blank
        self.profile.refresh_from_db()
        self.assertEqual(self.profile.token, "")

    # Login and test it redirects already logged in
    def test_login_redirects_to_checks(self):
        """
            Test user is only redirected to checks only once they have
            logged in.

            Alice is redirected to HTML form before login.
            On login, Alice is successfully redirected to hc-checks.
            asserts that the HTML form is returned with GET method.
            asserts that Alice is redirected to hc-checks.
        """
        # before login
        response = self.client.get(self.url)
        self.assertNotEqual(response.status_code, 302)
        self.assertTemplateUsed('accounts/check_token_submit.html')
        # after login
        self.client.post(self.url, follow=True)
        response = self.client.get(self.url)
        self.assertRedirects(response, reverse('hc-checks'))
        self.assertEqual(response.status_code, 302)

    # Todo: Login with a bad token and check that it redirects
    def test_bad_token_redirects(self):
        """
            Test a user is redirected to login when they supply a wrong token.

            Alice users with token = 'secret-token' uses 'bad-token' as token.
            Alice is redirected to login.
        """
        response = self.client.post(reverse('hc-check-token',
                                            args=('alice', 'bad_token')),
                                    follow=True)
        self.assertRedirects(response, reverse('hc-login'))

    # Todo: Any other tests?
