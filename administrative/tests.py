from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from administrative.models import *

# Create your tests here.

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

def create_beneficiary():
    beneficiary = Beneficiary.objects.create(id=1,
                                             name="Rodolfo",
                                             last_name_paternal="Rodriguez",
                                             last_name_maternal="Rocha",
                                             state="Querétaro",
                                             municipality="Peñamiller",
                                             community_name="Río Blanco",
                                             num_of_family_beneficiaries=16,
                                             contact_name="Juan",
                                             contact_phone="4424325671",
                                             account_number=123456,
                                             bank_name="Banamets")
    beneficiary.save()
    return beneficiary


class ProductionReportTest(TestCase):
    def test_new_report_only_selfconsumption(self):
        """
        Creating a new production report with correct information. Expecting a redirect to /administrative/
        """
        user = create_user()
        beneficiary = create_beneficiary()

        self.client.login(username="test", password="testpassword")
        response = self.client.post('/administrative/new_production_report/', {'self_seed': 1,
                                                                                'self_leaf': 3,
                                                                                'self_flour': 4,
                                                                                'days_per_month': 15
                                                                             })
        self.assertRedirects(response, '/administrative/', status_code=302, target_status_code=200, msg_prefix='', fetch_redirect_response=True)

    def test_new_report_complete(self):
        """
        Creating a new production report with correct and full information. Expecting a redirect to /administrative/
        """
        user = create_user()
        beneficiary = create_beneficiary()

        self.client.login(username="test", password="testpassword")
        response = self.client.post('/administrative/new_production_report/', {'self_seed': 1,
                                                                                'self_leaf': 3,
                                                                                'self_flour': 4,
                                                                                'days_per_month': 15,
                                                                                'exch_seed': 2,
                                                                                'want_for_seed': 'Hoja congelada',
                                                                                'exch_leaf': 3,
                                                                                'want_for_leaf': 'Hoja congelada'
                                                                             })
        #print("\n\n\n\n"+str(response))
        self.assertRedirects(response, '/administrative/', status_code=302, target_status_code=200, msg_prefix='', fetch_redirect_response=True)
