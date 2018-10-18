from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
from administrative.models import *
from profiles.models import *

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

def create_promoter():
    base_user = create_user()
    promoter = Promoter.objects.create(base_user=base_user,
                                        contact_name = "Contacto",
                                        contact_phone_number = "1234512312"
                                        )
    return promoter

def create_program():
    program = Program.objects.create(name="Productores")
    return program

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


class BeneficiariestTest(TestCase):
    def test_new_beneficary(self):
        """
        Creating a new beneficiary with correct information. Expecting a redirect to /administrative/beneficiaries

        """
        user = create_user()
        promoter = create_promoter()
        program = create_program()
        self.client.login(username="test", password="testpassword")
        response = self.client.post('/administrative/new_beneficiary/', {'name': 'beneTest',
                                                                                'last_name_paternal': 'Test',
                                                                                'last_name_maternal': 'Test',
                                                                                'num_of_family_beneficiaries': 5,
                                                                                'contact_name': 'contactTest',
                                                                                'contact_phone': '111111',
                                                                                'account_number': '222222',
                                                                                'bank_name': 'banco',
                                                                                'promoter': [promoter],
                                                                                'member_in': [program],
                                                                                'curp': '123FWEDWF12',
                                                                                'house_address': 'Casa 3',
                                                                                'house_references': 'Por ahí',
                                                                                'huerto_coordinates': 'Atrás'

                                                                             })
        self.assertRedirects(response, '/administrative/beneficiary/', status_code=302, target_status_code=200, msg_prefix='', fetch_redirect_response=True)

class CommunitiesTests(TestCase):
    def test_new_community(self):
        """
        Creating a new community. Expecting a redirect to /administrative/communities/

        """
        user = create_user()
        self.client.login(username="test", password="testpassword")
        response = self.client.post('/administrative/communities/', {'name': 'Río Blanco',
                                                                     'municipality': 'Peñamiller',
                                                                     'state': 'Querétaro',
                                                                    })
        self.assertRedirects(response, '/administrative/communities/', status_code=302, target_status_code=200, msg_prefix='', fetch_redirect_response=True)

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

class PaymentsTest(TestCase):
    def test_admin_no_pending_payments(self):
        """
        Admin checks pending payments buy there are none to be paid.
        """
        user = create_user()
        self.client.login(username="test", password="testpassword")
        response = self.client.get('/administrative/payments/')
        self.assertContains(response, "No hay pagos pendientes.")

    def test_admin_pending_payments(self):
        """
        Admin checks pending payments.
        """
        user = create_user()
        self.client.login(username="test", password="testpassword")

        user_p = User.objects.create_user('test_p', 'test_p@testuser.com', 'testpassword')
        base_user_p = BaseUser.objects.create(user=user_p, name="name",
                                            last_name_paternal="last_name_paternal",
                                            last_name_maternal="last_name_maternal",
                                            phone_number="phone_number",
                                            email="email@email.com",
                                            address="address")
        base_user_p.save()
        promoter = Promoter.objects.create(base_user=base_user_p,
                                            contact_name = "Contacto",
                                            contact_phone_number = "1234512312"
                                            )
        promoter.save()
        payment = Payment.objects.create(
                                            promoter=promoter,
                                            description="Pago por cultivo",
                                            quantity=1000,
                                            due_date=timezone.now() + timezone.timedelta(days=1)
                                        )
        payment.save()
        response = self.client.get('/administrative/payments/')
        self.assertContains(response, "Pago por cultivo")

    def test_pay_ok(self):
        user = create_user()
        self.client.login(username="test", password="testpassword")

        user_p = User.objects.create_user('test_p', 'test_p@testuser.com', 'testpassword')
        base_user_p = BaseUser.objects.create(user=user_p, name="name",
                                            last_name_paternal="last_name_paternal",
                                            last_name_maternal="last_name_maternal",
                                            phone_number="phone_number",
                                            email="email@email.com",
                                            address="address")
        base_user_p.save()
        promoter = Promoter.objects.create(base_user=base_user_p,
                                            contact_name = "Contacto",
                                            contact_phone_number = "1234512312"
                                            )
        promoter.save()
        payment = Payment.objects.create(
                                            promoter=promoter,
                                            description="Pago por cultivo",
                                            quantity=1000,
                                            due_date=timezone.now() + timezone.timedelta(days=1)
                                        )
        payment.save()
        pk = payment.pk
        data = {'comment': "This is a comment"}
        response = self.client.post('/administrative/pay/' +str(pk) + '/', data)
        self.assertContains(response, 'This is a comment')

class TrainingTests(TestCase):
    
