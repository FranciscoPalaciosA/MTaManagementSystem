from django.test import TestCase
from django.contrib.auth.models import User, Group
from django.urls import reverse
from profiles.models import *
from administrative.models import Community

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
        promoter.save()
        self.client.login(username="test", password="testpassword")
        response = self.client.post('/profiles/new_alert/', {'name': 'alert', 'description': 'alert description'})
        alerts = HelpAlert.objects.filter(promoter=promoter)
        self.assertEqual(len(alerts), 1)
        self.assertRedirects(response, '/profiles/', status_code=302, target_status_code=200, msg_prefix='', fetch_redirect_response=True)

    def test_add_new_alert_not_promoter(self):
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
        self.client.login(username="test", password="testpassword")
        response = self.client.post('/profiles/new_alert/', {'name': 'alert', 'description': 'alert description'})
        alerts = HelpAlert.objects.all()
        self.assertEqual(len(alerts), 0)
        self.assertRedirects(response, '/profiles/', status_code=302, target_status_code=200, msg_prefix='', fetch_redirect_response=True)

class NewUserTests(TestCase):
    def test_add_new_user(self):
        """
        Add a new base user
        """
        user = User.objects.create_user('test', 'test@testuser.com', 'testpassword')
        base_user = BaseUser.objects.create(user=user, name="name",
                                            last_name_paternal="last_name_paternal",
                                            last_name_maternal="last_name_maternal",
                                            phone_number="phone_number",
                                            email="email@email.com",
                                            address="address")
        base_user.save()
        group, created = Group.objects.get_or_create(name='test_group')
        user_info = {
                        "username": "testUser",
                        "password": "testpassword",
                        "group": group.id,
                        "name": "testName",
                        "last_name_paternal": "testLastnameP",
                        "last_name_maternal": "testLastnameM",
                        "phone_number": "4422497177",
                        "address": "test address #4",
                        "email": "test@email.com"}
        self.client.force_login(user)
        response = self.client.post('/profiles/new_user/', user_info)
        bu = BaseUser.objects.get(name='testName')
        self.assertEqual(bu.email, "test@email.com")
        self.assertRedirects(response, '/profiles/', status_code=302, target_status_code=200, msg_prefix='', fetch_redirect_response=True)

    def test_promoter_add_new_user(self):
        """
        Promoter tries to add a new user, should not be able to
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
        promoter.save()
        group, created = Group.objects.get_or_create(name='test_group')
        user_info = {
                        "username": "testUser",
                        "password": "testpassword",
                        "group": group.id,
                        "name": "testName",
                        "last_name_paternal": "testLastnameP",
                        "last_name_maternal": "testLastnameM",
                        "phone_number": "4422497177",
                        "address": "test address #4",
                        "email": "test@email.com"}
        self.client.force_login(user)
        response = self.client.post('/profiles/new_user/', user_info)
        bu = BaseUser.objects.filter()
        self.assertEqual(len(bu), 1)
        self.assertRedirects(response, '/administrative/', status_code=302, target_status_code=200, msg_prefix='', fetch_redirect_response=True)

    def test_add_new_promoter_with_one_community(self):
        """
        Add a new promoter
        """
        group, created = Group.objects.get_or_create(name='test_group')
        community = Community.objects.create(
                                                name ="community1",
                                                municipality = "mun1",
                                                state = "state1"
                                            )
        user = User.objects.create_user('test', 'test@testuser.com', 'testpassword')
        base_user = BaseUser.objects.create(user=user, name="name",
                                            last_name_paternal="last_name_paternal",
                                            last_name_maternal="last_name_maternal",
                                            phone_number="phone_number",
                                            email="email@email.com",
                                            address="address")
        base_user.save()
        user_info = {
                        "username": "testUser",
                        "password": "testpassword",
                        "group": group.id,
                        "name": "testName",
                        "last_name_paternal": "testLastnameP",
                        "last_name_maternal": "testLastnameM",
                        "phone_number": "4422497177",
                        "address": "test address #4",
                        "email": "test@email.com",
                        "contact_name": "testContactName",
                        "contact_phone_number": "testContactPhone",
                        "communities": community.id}
        #user to bypass @login_required
        self.client.force_login(user)
        response = self.client.post('/profiles/new_promoter/', user_info)
        p = Promoter.objects.filter(contact_name='testContactName')
        self.assertEqual(len(p), 1)
        self.assertRedirects(response, '/profiles/', status_code=302, target_status_code=200, msg_prefix='', fetch_redirect_response=True)

    def test_promoter_add_promoter(self):
        """
        Add a new promoter
        """
        group, created = Group.objects.get_or_create(name='test_group')
        community = Community.objects.create(
                                                name ="community1",
                                                municipality = "mun1",
                                                state = "state1"
                                            )
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
        promoter.save()
        user_info = {
                        "username": "testUser",
                        "password": "testpassword",
                        "group": group.id,
                        "name": "testName",
                        "last_name_paternal": "testLastnameP",
                        "last_name_maternal": "testLastnameM",
                        "phone_number": "4422497177",
                        "address": "test address #4",
                        "email": "test@email.com",
                        "contact_name": "testContactName",
                        "contact_phone_number": "testContactPhone",
                        "communities": community.id}
        #user to bypass @login_required
        self.client.force_login(user)
        response = self.client.post('/profiles/new_promoter/', user_info)
        p = Promoter.objects.all()
        self.assertEqual(len(p), 1)
        self.assertRedirects(response, '/administrative/', status_code=302, target_status_code=200, msg_prefix='', fetch_redirect_response=True)

    def test_add_new_promoter_with_multiple_communities(self):
        """
        Add a new promoter
        """
        user = User.objects.create_user('test', 'test@testuser.com', 'testpassword')
        base_user = BaseUser.objects.create(user=user, name="name",
                                            last_name_paternal="last_name_paternal",
                                            last_name_maternal="last_name_maternal",
                                            phone_number="phone_number",
                                            email="email@email.com",
                                            address="address")
        base_user.save()
        group, created = Group.objects.get_or_create(name='test_group')
        com1 = Community.objects.create(
                                    name ="community1",
                                    municipality = "mun1",
                                    state = "state1"
                                )
        com2 = Community.objects.create(
                                    name ="community2",
                                    municipality = "mun2",
                                    state = "state2"
                                )
        coms = [com1.id, com2.id]
        user_info = {
                        "username": "testUser",
                        "password": "testpassword",
                        "group": group.id,
                        "name": "testName",
                        "last_name_paternal": "testLastnameP",
                        "last_name_maternal": "testLastnameM",
                        "phone_number": "4422497177",
                        "address": "test address #4",
                        "email": "test@email.com",
                        "contact_name": "testContactName",
                        "contact_phone_number": "testContactPhone",
                        "communities": coms}
        #user to bypass @login_required
        self.client.force_login(user)
        response = self.client.post('/profiles/new_promoter/', user_info)
        p = Promoter.objects.filter(contact_name='testContactName')
        self.assertEqual(len(p), 1)
        self.assertRedirects(response, '/profiles/', status_code=302, target_status_code=200, msg_prefix='', fetch_redirect_response=True)
