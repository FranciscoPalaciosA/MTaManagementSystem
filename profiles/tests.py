from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from profiles.models import *

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
        Try to login with wrong user. Expecting a message saying the username and/or password are wrong
        """
        user = User.objects.create_user('test', 'test@testuser.com', 'testpassword')
        response = self.client.post('/accounts/login/', {'username': 'testWrong', 'password': 'testpassword'})
        self.assertContains(response, "El usuario y/o contraseña son incorrectos.")

class AlertTests(TestCase):
    def test_add_new_alert(self):
        """
        Add a new alert
        """
        user = User.objects.create_user('test', 'test@testuser.com', 'testpassword')
        base_user = BaseUser.objects.create(user=user, name="name",
                                            last_name_paternal="last_name_paternal",
                                            last_name_maternal="last_name_maternal",
                                            phone_number="phone_number",
                                            email="email@email.com",
                                            address="address")
        base_user.save()
        promoter = Promoter.objects.create(base_user=base_user,
                                            contact_name="asdfasdf",
                                            contact_phone_number="4422234")

        self.client.login(username="test", password="testpassword")
        response = self.client.post('/profiles/new_alert/', {'name': 'alert', 'description': 'alert description'})
        self.assertRedirects(response, '/profiles/', status_code=302, target_status_code=200, msg_prefix='', fetch_redirect_response=True)














#ll
