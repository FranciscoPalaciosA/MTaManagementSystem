from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from administrative.models import *

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

class ProductionReportTest(TestCase):
    def test_new_report_only_selfconsumption(self):
        """
        Creating a new production report with correct information. Expecting a redirect to /administrative/
        """
        user = create_user()
        self.client.login(username="test", password="testpassword")
        response = self.client.post('/administrative/new_production_report', {'self_seed': 1,
                                                                                'self_leaf': 3,
                                                                                'self_flour': 4,
                                                                                'days_per_month': 15
                                                                             })
        #print("\n\n\n\n"+response)
        self.assertRedirects(response, '/administrative/', status_code=301, target_status_code=200, msg_prefix='', fetch_redirect_response=True)


#'exch_seed': 2,
#'want_for_seed': 'Hoja congelada',
#'exch_leaf': 3,
#'want_for_leaf': 'Hoja congelada'

class BeneficiariestTest(TestCase):
    def test_new_beneficary_only_selfconsumption(self):
        """
        Creating a new beneficiary with correct information. Expecting a redirect to /administrative/beneficiaries

        """
        user = create_user()
        self.client.login(username="test", password="testpassword")
        response = self.client.post('/administrative/new_beneficiary', {'name': 'beneTest',
                                                                                'last_name_paternal': 'Test',
                                                                                'last_name_maternal': 'Test',
                                                                                'state': 'testState',
                                                                                'municipality': 'muniTest',
                                                                                'community_name' : 'testComm',
                                                                                'num_of_family_beneficiaries': 5,
                                                                                'contact_name': 'contactTest',
                                                                                'contact_phone': '111111',
                                                                                'account_number': '222222',
                                                                                'bank_name': 'banco'
                                                                             })
        #print("\n\n\n\n"+response)
        self.assertRedirects(response, '/administrative/beneficiaries', status_code=301, target_status_code=200, msg_prefix='', fetch_redirect_response=True)


class WeeklySessionTests(TestCase):
    def test_add_new_weekly_session(self):
        """
        Register a weekly session
        """
        user = create_user()
        promoter = Promoter.objects.create(base_user=user,
                                           contact_name="Juan",
                                           contact_phone_number="44222345678")
        promoter.save()

        beneficiary = Beneficiary.objects.create(promoter_id=1,
                                                 name="Rodolfo",
                                                 last_name_paternal="Rodriguez",
                                                 last_name_maternal="Rocha",
                                                 state="Querétaro",
                                                 municipality="Peñamiller",
                                                 community_name="Río Blanco",
                                                 num_of_family_beneficiaries=16,
                                                 contact_name="Juan",
                                                 contact_phone="4325671",
                                                 account_number=123456,
                                                 bank_name="Banamets")
        beneficiary.save()

        self.client.login(username="test", password="testpassword")
        response = self.client.post('/administrative/weekly_sessions/', {'type': 'session_type',
                                                                         'topic': 'session_topic',
                                                                         'assistants': 1,
                                                                         'start_time': '4:00 PM',
                                                                         'end_time': '5:00 PM',
                                                                         'promoter_id': 1})
        self.assertRedirects(response, '/administrative/weekly_sessions/', status_code=302, target_status_code=200, msg_prefix='', fetch_redirect_response=True)
