from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
from administrative.models import *
from profiles.models import *
import datetime

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
        user = User.objects.create_user('user', 'user@testuser.com', 'testpassword')
        base_user = BaseUser.objects.create(user=user, name="name",
                                            last_name_paternal="last_name_paternal",
                                            last_name_maternal="last_name_maternal",
                                            phone_number="phone_number",
                                            email="email@email.com",
                                            address="address")
        base_user.save()

        user_promoter = User.objects.create_user('promoter', 'promoter@testuser.com', 'testpassword')
        base_user_promoter = BaseUser.objects.create(user=user_promoter, name="PromotoraTest",
                                                        last_name_paternal="last_name_paternal",
                                                        last_name_maternal="last_name_maternal",
                                                        phone_number="phone_number",
                                                        email="email@email.com",
                                                        address="address")
        base_user_promoter.save()

        community = Community.objects.create(name = 'Name',
                                            municipality = 'Municipality',
                                            state = 'State')

        promoter = Promoter.objects.create(base_user=base_user_promoter,
                                            contact_name = "Contacto",
                                            contact_phone_number = "1234512312"
                                            )
        promoter.save()

        beneficiary = Beneficiary.objects.create(name="Rodolfo",
                                                 last_name_paternal="Rodriguez",
                                                 last_name_maternal="Rocha",
                                                 community=community,
                                                 promoter=promoter,
                                                 num_of_family_beneficiaries=16,
                                                 contact_name="Juan",
                                                 contact_phone="4424325671",
                                                 account_number=123456,
                                                 bank_name="Banamets")
        beneficiary.save()

        self.client.login(username="promoter", password="testpassword")

        response = self.client.post('/administrative/weekly_sessions/', {'date': datetime.date.today().strftime('%d-%m-%Y'),
                                                                         'type': 'session_type',
                                                                         'topic': 'session_topic',
                                                                         'assistants': 1,
                                                                         'start_time': '4:00 PM',
                                                                         'end_time': '5:00 PM',
                                                                         'promoter_id': [promoter.id]})
        self.assertRedirects(response, '/administrative/weekly_sessions/', status_code=302, target_status_code=200, msg_prefix='', fetch_redirect_response=True)

        weekly_session = WeeklySession.objects.get(promoter=promoter)
        assistant = weekly_session.assistants.get()

        self.assertEqual(weekly_session.type, 'session_type')
        self.assertEqual(weekly_session.topic, 'session_topic')
        self.assertEqual(weekly_session.start_time, '4:00 PM')
        self.assertEqual(weekly_session.end_time, '5:00 PM')
        self.assertEqual(assistant, beneficiary)

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

    def test_promoter_checks_has_payments(self):
        promoter = create_promoter()
        promoter.save()
        self.client.login(username="test", password="testpassword")
        payment = Payment.objects.create(
                                            promoter=promoter,
                                            description="Pago por cultivo",
                                            quantity=1000,
                                            due_date=timezone.now() + timezone.timedelta(days=1)
                                        )
        payment.save()
        response = self.client.get('/administrative/payments/')
        self.assertContains(response, "Pago por cultivo")
    def test_admin_add_payment(self):
        user = User.objects.create_user('test_1', 'test_1@testuser.com', 'testpassword')
        base_user = BaseUser.objects.create(user=user, name="name",
                                            last_name_paternal="last_name_paternal",
                                            last_name_maternal="last_name_maternal",
                                            phone_number="phone_number",
                                            email="email@email.com",
                                            address="address")
        base_user.save()
        self.client.login(username="test_1", password="testpassword")
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
        data = {
            'promoter': promoter.id,
            'description': 'razon de pago',
            'quantity': 1000,
            'due_date': '10/10/2018'
        }
        response = self.client.post('/administrative/add_payment/', data)
        self.assertRedirects(response, '/administrative/payments/', status_code=302, target_status_code=200, msg_prefix='', fetch_redirect_response=True)
        payment = Payment.objects.filter(promoter=promoter)[0]
        self.assertEquals(payment.description,'razon de pago' )

    def test_promoter_add_payment(self):
        user = create_promoter()
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
        data = {
            'promoter': promoter.id,
            'description': 'razon de pago',
            'quantity': 1000,
            'due_date': '10/10/2018'
        }
        response = self.client.post('/administrative/add_payment/', data)
        self.assertRedirects(response, '/administrative/', status_code=302, target_status_code=200, msg_prefix='', fetch_redirect_response=True)
        payment = Payment.objects.filter(promoter=promoter)
        self.assertEquals(len(payment),0 )

    def test_admin_resolve_payment(self):
        user = User.objects.create_user('test_1', 'test_1@testuser.com', 'testpassword')
        base_user = BaseUser.objects.create(user=user, name="name",
                                            last_name_paternal="last_name_paternal",
                                            last_name_maternal="last_name_maternal",
                                            phone_number="phone_number",
                                            email="email@email.com",
                                            address="address")
        base_user.save()
        self.client.login(username="test_1", password="testpassword")

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
        response = self.client.post('/administrative/pay/' + str(payment.id) + '/', {'comment':'comment'})
        p = Payment.objects.get(promoter=promoter)
        self.assertEqual(p.comment, 'comment')

    def test_promoter_resolve_payment(self):
        prom = create_promoter()
        prom.save()
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
        response = self.client.post('/administrative/pay/' + str(payment.id) + '/', {'comment':'comment'})
        p = Payment.objects.get(promoter=promoter)
        #Payment did not update
        self.assertEqual(p.comment, '')

class NewSavingAccount(TestCase):
    def test_add_new_saving_account_with_one_beneficiary(self):
        """
        Creating a new sabing account. Expecting a redirect to /administrative/

        """
        user = create_user()
        self.client.login(username="test", password="testpassword")
        beneficiary = Beneficiary.objects.create(promoter_id=1,
                                                 name="Rodolfo",
                                                 last_name_paternal="Rodriguez",
                                                 last_name_maternal="Rocha",
                                                 num_of_family_beneficiaries=16,
                                                 contact_name="Juan",
                                                 contact_phone="4325671",
                                                 account_number=123456,
                                                 bank_name="Banamets")
        beneficary.save()
        response = self.client.post('/administrative/new_saving_account/', {'name': 'beneTest',
                                                                                "name": "testAccount",
                                                                                "community": "testCommunity",
                                                                                "municipality": "testMunicipality",
                                                                                "location": "testLocation",
                                                                                "list_of_beneficiaries": beneficiary.id,
                                                                                "total saved ammount": "222222",
                                                                                "president_beneficiary": beneficiary.id,
                                                                                "treasurer_beneficiary": beneficiary.id,
                                                                                "partner_beneficiary": beneficiary.id
                                                                             })
        self.assertRedirects(response, '/administrative/', status_code=302, target_status_code=200, msg_prefix='', fetch_redirect_response=True)
    def test_add_new_saving_account_with_multiple_beneficiaries(self):
        """
        Creating a new sabing account. Expecting a redirect to /administrative/

        """
        user = create_user()
        self.client.login(username="test", password="testpassword")
        beneficiary1 = Beneficiary.objects.create(
                                                 name="Rodolfo",
                                                 last_name_paternal="Rodriguez",
                                                 last_name_maternal="Rocha",
                                                 num_of_family_beneficiaries=16,
                                                 contact_name="Juan",
                                                 contact_phone="4325671",
                                                 account_number=123456,
                                                 bank_name="Banamets")
        beneficiary1.save()
        beneficiary2 = Beneficiary.objects.create(
                                                 name="Juan",
                                                 last_name_paternal="Rodriguez",
                                                 last_name_maternal="Rocha",
                                                 num_of_family_beneficiaries=15,
                                                 contact_name="José",
                                                 contact_phone="4325671",
                                                 account_number=123456,
                                                 bank_name="Bankomer")
        beneficiary2.save()
        beneficiary3 = Beneficiary.objects.create(
                                                 name="Jose",
                                                 last_name_paternal="Rodriguez",
                                                 last_name_maternal="Rocha",
                                                 num_of_family_beneficiaries=15,
                                                 contact_name="José",
                                                 contact_phone="4325671",
                                                 account_number=123456,
                                                 bank_name="Bankomer")
        beneficiary3.save()
        beneficiaries = [beneficiary1.id,beneficiary2.id,beneficiary3.id]
        response = self.client.post('/administrative/new_saving_account/', {'name': 'beneTest',
                                                                                "name": "testAccount",
                                                                                "community": "testCommunity",
                                                                                "municipality": "testMunicipality",
                                                                                "location": "testLocation",
                                                                                "list_of_beneficiaries": beneficiaries,
                                                                                "total saved ammount": "222222",
                                                                                "president_beneficiary": beneficiary1.id,
                                                                                "treasurer_beneficiary": beneficiary2.id,
                                                                                "partner_beneficiary": beneficiary3.id
                                                                             })
        self.assertRedirects(response, '/administrative/', status_code=302, target_status_code=200, msg_prefix='', fetch_redirect_response=True)

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
    def test_new_training(self):
        user = create_user()
        self.client.login(username="test", password="testpassword")
        beneficiary = create_beneficiary()
