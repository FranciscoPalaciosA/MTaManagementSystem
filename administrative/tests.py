from django.test import TestCase
from django.contrib.auth.models import User, Group
from django.urls import reverse
from django.utils import timezone
from administrative.models import *
from profiles.models import *
import datetime

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


class CommunityTests(TestCase):
    def test_view_uses_correct_template_for_administrative_assistant(self):
        """
        An adminstrative_assistant enters /administrative/communities/ and the correct template loads
        """
        user = User.objects.create_user('user', 'user@testuser.com', 'testpassword')
        base_user = BaseUser.objects.create(user=user, name="name",
                                            last_name_paternal="last_name_paternal",
                                            last_name_maternal="last_name_maternal",
                                            phone_number="phone_number",
                                            email="email@email.com",
                                            address="address")
        base_user.save()

        group, created = Group.objects.get_or_create(name='Asistente Administrativo')
        user.groups.add(group)

        self.client.login(username="user", password="testpassword")

        response = self.client.get('/administrative/communities/')
        self.assertTemplateUsed(response, 'administrative/communities.html')

    def test_view_uses_correct_template_for_administrative_coordinator(self):
        """
        An adminstrative_coordinator enters /administrative/communities/ and the correct template loads
        """
        user = User.objects.create_user('user', 'user@testuser.com', 'testpassword')
        base_user = BaseUser.objects.create(user=user, name="name",
                                            last_name_paternal="last_name_paternal",
                                            last_name_maternal="last_name_maternal",
                                            phone_number="phone_number",
                                            email="email@email.com",
                                            address="address")
        base_user.save()

        group, created = Group.objects.get_or_create(name='Coordinador Administrativo')
        user.groups.add(group)

        self.client.login(username="user", password="testpassword")

        response = self.client.get('/administrative/communities/')
        self.assertTemplateUsed(response, 'administrative/communities.html')

    def test_administrative_assistant_adds_new_community(self):
        """
        An administrative assistant registers a new community

        """
        user = User.objects.create_user('user', 'user@testuser.com', 'testpassword')
        base_user = BaseUser.objects.create(user=user, name="name",
                                            last_name_paternal="last_name_paternal",
                                            last_name_maternal="last_name_maternal",
                                            phone_number="phone_number",
                                            email="email@email.com",
                                            address="address")
        base_user.save()

        group, created = Group.objects.get_or_create(name='Asistente Administrativo')
        user.groups.add(group)

        self.client.login(username="user", password="testpassword")

        response = self.client.post('/administrative/communities/', {'name': 'Río Blanco',
                                                                     'municipality': 'Peñamiller',
                                                                     'state': 'Querétaro',
                                                                    })
        self.assertRedirects(response, '/administrative/communities/', status_code=302, target_status_code=200, msg_prefix='', fetch_redirect_response=True)
        community = Community.objects.get(name='Río Blanco')
        self.assertEqual(community.municipality, 'Peñamiller')
        self.assertEqual(community.state, 'Querétaro')

    def test_promoter_cant_access(self):
        """
        A promoter enters /administrative/communities/ and is redirected
        """
        user = User.objects.create_user('promoter', 'promoter@testuser.com', 'testpassword')
        base_user_promoter = BaseUser.objects.create(user=user, name="PromotoraTest",
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

        group, created = Group.objects.get_or_create(name='promoter')
        user.groups.add(group)

        self.client.login(username="promoter", password="testpassword")

        response = self.client.get('/administrative/communities/')
        self.assertRedirects(response, '/administrative/', status_code=302, target_status_code=200, msg_prefix='', fetch_redirect_response=True)

    def test_administrative_coordinator_adds_new_community(self):
        """
        An administrative coordinator registers a new community

        """
        user = User.objects.create_user('user', 'user@testuser.com', 'testpassword')
        base_user = BaseUser.objects.create(user=user, name="name",
                                            last_name_paternal="last_name_paternal",
                                            last_name_maternal="last_name_maternal",
                                            phone_number="phone_number",
                                            email="email@email.com",
                                            address="address")
        base_user.save()

        group, created = Group.objects.get_or_create(name='Coordinador Administrativo')
        user.groups.add(group)

        self.client.login(username="user", password="testpassword")

        response = self.client.post('/administrative/communities/', {'name': 'Río Blanco',
                                                                     'municipality': 'Peñamiller',
                                                                     'state': 'Querétaro',
                                                                    })
        self.assertRedirects(response, '/administrative/communities/', status_code=302, target_status_code=200, msg_prefix='', fetch_redirect_response=True)
        community = Community.objects.get(name='Río Blanco')
        self.assertEqual(community.municipality, 'Peñamiller')
        self.assertEqual(community.state, 'Querétaro')

class WeeklySessionTests(TestCase):
    def test_view_uses_correct_template_for_administrative_assistant(self):
        """
        An adminstrative_ enters /administrative/weekly_sessions/ and the correct template loads
        """
        user = User.objects.create_user('user', 'user@testuser.com', 'testpassword')
        base_user = BaseUser.objects.create(user=user, name="name",
                                            last_name_paternal="last_name_paternal",
                                            last_name_maternal="last_name_maternal",
                                            phone_number="phone_number",
                                            email="email@email.com",
                                            address="address")
        base_user.save()

        group, created = Group.objects.get_or_create(name='Asistente Administrativo')
        user.groups.add(group)

        self.client.login(username="user", password="testpassword")

        response = self.client.get('/administrative/weekly_sessions/')
        self.assertTemplateUsed(response, 'administrative/Admin_weekly_sessions.html')

    def test_view_uses_correct_template_for_administrative_coordinator(self):
        """
        An adminstrative_ enters /administrative/weekly_session/ and the correct template loads
        """
        user = User.objects.create_user('user', 'user@testuser.com', 'testpassword')
        base_user = BaseUser.objects.create(user=user, name="name",
                                            last_name_paternal="last_name_paternal",
                                            last_name_maternal="last_name_maternal",
                                            phone_number="phone_number",
                                            email="email@email.com",
                                            address="address")
        base_user.save()

        group, created = Group.objects.get_or_create(name='Coordinador Administrativo')
        user.groups.add(group)

        self.client.login(username="user", password="testpassword")

        response = self.client.get('/administrative/weekly_sessions/')
        self.assertTemplateUsed(response, 'administrative/Admin_weekly_sessions.html')

    def test_view_uses_correct_template_for_promoter(self):
        """
        A promoter enters /administrative/weekly_sessions/ and the correct template loads
        """
        user = User.objects.create_user('promoter', 'promoter@testuser.com', 'testpassword')
        base_user_promoter = BaseUser.objects.create(user=user, name="PromotoraTest",
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

        group, created = Group.objects.get_or_create(name='promoter')
        user.groups.add(group)

        self.client.login(username="promoter", password="testpassword")

        response = self.client.get('/administrative/weekly_sessions/')
        self.assertTemplateUsed(response, 'administrative/weekly_sessions.html')

    def test_promoter_adds_new_weekly_session(self):
        """
        Promoter registers a weekly session
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

        group, created = Group.objects.get_or_create(name='promoter')
        user.groups.add(group)

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
                                                                         'topic': 'session_topicS',
                                                                         'assistants': 1,
                                                                         'start_time': '4:00 PM',
                                                                         'end_time': '5:00 PM',
                                                                         'promoter_id': [promoter.id]})
        self.assertRedirects(response, '/administrative/weekly_sessions/', status_code=302, target_status_code=200, msg_prefix='', fetch_redirect_response=True)

        weekly_session = WeeklySession.objects.get(promoter=promoter)
        assistant = weekly_session.assistants.get()

        self.assertEqual(weekly_session.type, 'session_type')
        self.assertEqual(weekly_session.start_time, '4:00 PM')
        self.assertEqual(weekly_session.end_time, '5:00 PM')
        self.assertEqual(assistant, beneficiary)

    def test_promoter_checks_log_has_no_past_sessions(self):
        """
        Promoter checks previous weekly sessions buy there are none
        """
        user = User.objects.create_user('promoter', 'promoter@testuser.com', 'testpassword')
        base_user_promoter = BaseUser.objects.create(user=user, name="PromotoraTest",
                                                        last_name_paternal="last_name_paternal",
                                                        last_name_maternal="last_name_maternal",
                                                        phone_number="phone_number",
                                                        email="email@email.com",
                                                        address="address")
        base_user_promoter.save()

        promoter = Promoter.objects.create(base_user=base_user_promoter,
                                            contact_name = "Contacto",
                                            contact_phone_number = "1234512312"
                                            )
        promoter.save()

        group, created = Group.objects.get_or_create(name='promoter')
        user.groups.add(group)

        self.client.login(username="promoter", password="testpassword")

        response = self.client.get('/administrative/weekly_sessions/')
        self.assertContains(response, "No hay sesiones pasadas")

    def test_promoter_checks_log_has_past_sessions(self):
        """
        Promoter checks previous weekly sessions and there are
        """
        user = User.objects.create_user('promoter', 'promoter@testuser.com', 'testpassword')
        user.save()

        base_user_promoter = BaseUser.objects.create(user=user, name="PromotoraTest",
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

        group, created = Group.objects.get_or_create(name='promoter')
        user.groups.add(group)

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

        weekly_session = WeeklySession.objects.create(date = datetime.date.today(),
                                                      type = "session_type",
                                                      topic = "session_topic",
                                                      start_time = "4:00 PM",
                                                      end_time = "5:00 PM",
                                                      promoter = promoter)
        weekly_session.assistants.add(beneficiary)

        self.client.login(username="promoter", password="testpassword")

        response = self.client.get('/administrative/weekly_sessions/')
        self.assertContains(response, "session_type")
        self.assertContains(response, "session_topic")

    def test_administrative_checks_log_has_no_past_sessions(self):
        """
        An administrative checks previous weekly sessions buy there are none
        """
        user = User.objects.create_user('user', 'user@testuser.com', 'testpassword')
        base_user = BaseUser.objects.create(user=user, name="name",
                                            last_name_paternal="last_name_paternal",
                                            last_name_maternal="last_name_maternal",
                                            phone_number="phone_number",
                                            email="email@email.com",
                                            address="address")
        base_user.save()

        group, created = Group.objects.get_or_create(name='Asistente Administrativo')
        user.groups.add(group)

        self.client.login(username="user", password="testpassword")

        response = self.client.get('/administrative/weekly_sessions/')
        self.assertContains(response, "No hay sesiones pasadas")

    def test_promoter_checks_log_has_past_sessions(self):
        """
        A promoter check previous weekly sessions and there are
        """
        user = User.objects.create_user('promoter', 'promoter@testuser.com', 'testpassword')
        base_user_promoter = BaseUser.objects.create(user=user, name="PromotoraTest",
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

        group, created = Group.objects.get_or_create(name='promoter')
        user.groups.add(group)

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

        weekly_session = WeeklySession.objects.create(date = datetime.date.today(),
                                                      type = "session_type",
                                                      topic = "session_topic",
                                                      start_time = "4:00 PM",
                                                      end_time = "5:00 PM",
                                                      promoter = promoter)
        weekly_session.assistants.add(beneficiary)

        self.client.login(username="promoter", password="testpassword")

        response = self.client.get('/administrative/weekly_sessions/')
        self.assertContains(response, "session_type")
        self.assertContains(response, "session_topic")

class PaymentsTests(TestCase):
    def test_view_uses_correct_template_for_administrative(self):
        """
        An adminstrative enters /administrative/payments/ and the correct template loads
        """
        user = User.objects.create_user('user', 'user@testuser.com', 'testpassword')
        base_user = BaseUser.objects.create(user=user, name="name",
                                            last_name_paternal="last_name_paternal",
                                            last_name_maternal="last_name_maternal",
                                            phone_number="phone_number",
                                            email="email@email.com",
                                            address="address")
        base_user.save()

        group, created = Group.objects.get_or_create(name='Asistente Administrativo')
        user.groups.add(group)

        self.client.login(username="user", password="testpassword")

        response = self.client.get('/administrative/payments/')
        self.assertTemplateUsed(response, 'administrative/Admin_payments.html')

    def test_view_uses_correct_template_for_promoter(self):
        """
        A promoter enters /administrative/payments/ and the correct template loads
        """
        user = User.objects.create_user('promoter', 'promoter@testuser.com', 'testpassword')
        base_user_promoter = BaseUser.objects.create(user=user, name="PromotoraTest",
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

        group, created = Group.objects.get_or_create(name='promoter')
        user.groups.add(group)

        self.client.login(username="promoter", password="testpassword")

        response = self.client.get('/administrative/payments/')
        self.assertTemplateUsed(response, 'administrative/payments.html')

    def test_admin_no_pending_payments(self):
        """
        Admin checks pending payments buy there are none to be paid.
        """
        user = User.objects.create_user('test', 'test@testuser.com', 'testpassword')
        user.save()
        base_user = BaseUser.objects.create(user=user, name="name",
                                            last_name_paternal="last_name_paternal",
                                            last_name_maternal="last_name_maternal",
                                            phone_number="phone_number",
                                            email="email@email.com",
                                            address="address")
        base_user.save()

        group, created = Group.objects.get_or_create(name='Asistente Administrativo')
        user.groups.add(group)

        self.client.login(username="test", password="testpassword")
        response = self.client.get('/administrative/payments/')
        self.assertContains(response, "No hay pagos pendientes.")

    def test_admin_pending_payments(self):
        """
        Admin checks pending payments.
        """
        user = create_user()

        user_p = User.objects.create_user('promoter', 'test_p@testuser.com', 'testpassword')
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

        self.client.login(username="test", password="testpassword")
        response = self.client.get('/administrative/payments/')
        self.assertContains(response, "Pago por cultivo")

    def test_promoter_upcoming_payments(self):
        """
        Promoter checks upcoming payments.
        """
        user = User.objects.create_user('promoter', 'test_p@testuser.com', 'testpassword')
        base_user_p = BaseUser.objects.create(user=user, name="name",
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

        group, created = Group.objects.get_or_create(name='promoter')
        user.groups.add(group)

        self.client.login(username="promoter", password="testpassword")

        response = self.client.get('/administrative/payments/')
        self.assertContains(response, "Pago por cultivo")

    def test_promoter_past_payments(self):
        """
        Promoter checks past payments.
        """
        user = User.objects.create_user('promoter', 'test_p@testuser.com', 'testpassword')
        base_user_p = BaseUser.objects.create(user=user, name="name",
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
                                            due_date=timezone.now() + timezone.timedelta(days=1),
                                            pay_date=timezone.now() + timezone.timedelta(days=1)
                                        )
        payment.save()

        group, created = Group.objects.get_or_create(name='promoter')
        user.groups.add(group)

        self.client.login(username="promoter", password="testpassword")
        response = self.client.get('/administrative/payments/')
        self.assertContains(response, "Pago por cultivo")

    def test_administrative_assistant_add_payment(self):
        user = User.objects.create_user('test_1', 'test_1@testuser.com', 'testpassword')
        base_user = BaseUser.objects.create(user=user, name="name",
                                            last_name_paternal="last_name_paternal",
                                            last_name_maternal="last_name_maternal",
                                            phone_number="phone_number",
                                            email="email@email.com",
                                            address="address")
        base_user.save()

        group, created = Group.objects.get_or_create(name='Asistente Administrativo')
        user.groups.add(group)

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

    def test_administrative_coordinator_add_payment(self):
        user = User.objects.create_user('test_1', 'test_1@testuser.com', 'testpassword')
        base_user = BaseUser.objects.create(user=user, name="name",
                                            last_name_paternal="last_name_paternal",
                                            last_name_maternal="last_name_maternal",
                                            phone_number="phone_number",
                                            email="email@email.com",
                                            address="address")
        base_user.save()

        group, created = Group.objects.get_or_create(name='Coordinador Administrativo')
        user.groups.add(group)

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
