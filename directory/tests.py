from django.test import TestCase
from django.urls import reverse
from .models import *

class WeeklySessionTests(TestCase):
    def test_add_new_weekly_session(self):
        """
        Register a weekly session
        """
        user = User.objects.create_user('test', 'test@testuser.com', 'testpassword')
        base_user = BaseUser.objects.create(user=user,
                                            name="name",
                                            last_name_paternal="last_name_paternal",
                                            last_name_maternal="last_name_maternal",
                                            phone_number="phone_number",
                                            email="email@email.com",
                                            address="address")
        base_user.save()

        promoter = Promoter.objects.create(base_user=base_user,
                                           contact_name="Juan",
                                           contact_phone_number="44222345678")
        promoter.save()

        beneficiary = Beneficiary.objects.create(id=1,
                                                 name="Rodolfo",
                                                 last_name_paternal="Rodriguez",
                                                 last_name_maternal="Rocha",
                                                 state="Querétaro",
                                                 municipality="Peñamiller",
                                                 community_name="Río Blanco",
                                                 num_of_family_beneficiaries=16,
                                                 contact_name="Juan"
                                                 contact_phone="4424325671"
                                                 account_number=123456
                                                 bank_name="Banamets")
        beneficiary.save()

        self.client.login(username="test", password="testpassword")
        response = self.client.post('/administrative/weekly_sessions/', {'type': 'session_type', 'topic': 'session_topic', 'assistants': beneficiary, 'start_time': '4:00 PM', 'end_time': '5:00 PM'})
        self.assertRedirects(response, '/administrative/weekly_sessions/', status_code=302, target_status_code=200, msg_prefix='', fetch_redirect_response=True)
