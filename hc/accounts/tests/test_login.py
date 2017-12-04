from django.contrib.auth.models import User
from django.core import mail
from django.test import TestCase
from hc.api.models import Check
from django.urls import reverse
from hc.accounts.forms import EmailPasswordForm

class LoginTestCase(TestCase):

    def setUp(self):
        self.url = reverse('hc-login')
        self.check = Check()
        self.form = {"email": "alice@example.org"}
        self.wrong_credentials = {"email": "wrong@email.com", "password": "wrongpassword"}
        
    def test_it_sends_link(self):
        self.check.save()
        session = self.client.session
        session["welcome_code"] = str(self.check.code)
        session.save()

        response = self.client.post(self.url, self.form)
        assert response.status_code == 302

        ### Assert that a user was created
        self.assertEqual(User.objects.count(), 1)

        # And email sent
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, 'Log in to healthchecks.io')

        ### Assert contents of the email body
        created_user = User.objects.first()
        self.assertTrue(len(mail.outbox[0].body) > 0)
        self.assertIn(created_user.username, mail.outbox[0].body)

        ### Assert that check is associated with the new user
        check_user = Check.objects.first().user
        self.assertEqual(check_user.username, created_user.username)

    def test_it_pops_bad_link_from_session(self):
        self.client.session["bad_link"] = True
        self.client.get(self.url)
        assert "bad_link" not in self.client.session

        ### Any other tests?
    def test_login_returns_form_for_get(self):
        r = self.client.get(self.url)
        self.assertTemplateUsed('accounts/login.html')
        self.assertEqual(EmailPasswordForm, r.context['form'].__class__)

    def test_redirect_with_successful_login(self):
        r = self.client.post(self.url, self.form, follow=True)
        self.assertRedirects(r, reverse('hc-login-link-sent'))

    def test_login_with_incorrect_password(self):
        r = self.client.post(self.url, self.wrong_credentials)
        # bad_credentials should be True in the context
        self.assertTrue(r.context['bad_credentials'] is True)
        self.assertContains(r, 'Incorrect email or password')

        # assert no such user exists in the database at all.
        with self.assertRaises(User.DoesNotExist):
            User.objects.get(email=self.wrong_credentials["email"])

    def test_login_link_cannot_be_used_twice(self):
        r = self.client.post(self.url, self.form)
        login_link = r.context['login_link']

        # make first request.
        self.client.post(login_link)

        # logout user.
        self.client.get(reverse('hc-logout'))

        # login again with the same login link.
        r = self.client.post(login_link)
        self.assertRedirects(r, reverse('hc-login'))