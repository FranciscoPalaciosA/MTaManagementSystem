from django.test import TestCase
from django.urls import reverse
from .models import *

def create_user():
    user = User.objects.create_user('test', 'test@testuser.com', 'testpassword')
    base_user = BaseUser.objects.create(user=user, name="name",
                                        last_name_paternal="last_name_paternal",
                                        last_name_maternal="last_name_maternal",
                                        phone_number="phone_number",
                                        email="email@email.com",
                                        address="address")
    base_user.save()
    return base_user

class AddContactTest(TestCase):

    def test_new_beneficary_only_selfconsumption(self):
        """
        Creating a new contact with correct information. Expecting a redirect to /directory/
        """
        user = create_user()
        self.client.login(username="test", password="testpassword")
        response = self.client.post('/administrative/new_contact', {'first_name': 'contact',
                                                                                'last_name_paternal': 'Test',
                                                                                'last_name_maternal': 'Test',
                                                                                'phone_number': '123456',
                                                                                'email': 'contact@test.com'
                                                                                'contact_type':'Voluntario',
                                                                                'institution':'INEGI',
                                                                                'comments': 'test'
                                                                             })
        #print("\n\n\n\n"+response)

        self.assertRedirects(response, '/directory/', status_code=301, target_status_code=200, msg_prefix='', fetch_redirect_response=True)
