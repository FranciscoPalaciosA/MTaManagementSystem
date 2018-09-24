from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse

# Create your tests here.
class LoginTests(TestCase):
    def test_login_with_existing_user(self):
        """
        Try to login with an existing user. Expecting a redirect to /directory/
        """
        user = User.objects.create_user('test', 'test@testuser.com', 'testpassword')
        response = self.client.post('/accounts/login/', {'username': 'test', 'password': 'testpassword'})
        self.assertRedirects(response, '/directory/', status_code=302, target_status_code=200, msg_prefix='', fetch_redirect_response=True)

    def test_login_with_wrong_credentials(self):
        """
        Try to login with wrong user. Expecting a redirect to /directory/
        """
        user = User.objects.create_user('test', 'test@testuser.com', 'testpassword')
        response = self.client.post('/accounts/login/', {'username': 'testWrong', 'password': 'testpassword'})
        self.assertContains(response, "El usuario y/o contraseña son incorrectos.")
