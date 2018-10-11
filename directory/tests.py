from django.test import TestCase
from django.urls import reverse
from .models import *

lass AddContactTest(TestCase):

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
                                                                                'institution':'INEGI'
                                                                             })
        #print("\n\n\n\n"+response)

        self.assertRedirects(response, '/directory/', status_code=301, target_status_code=200, msg_prefix='', fetch_redirect_response=True)
