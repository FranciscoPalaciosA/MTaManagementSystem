from django.test import TestCase
from django.contrib.auth.models import User, Group
from django.urls import reverse
from django.utils import timezone
from administrative.models import *
from profiles.models import *


def create_database():
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


def create_user_for_group(group_name):
    user = User.objects.create_user(group_name, 'fieldtech@testuser.com', 'testpassword')
    group, created = Group.objects.get_or_create(name=group_name)
    user.groups.add(group)
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

        self.client.login(username="user", password="testpassword")
        response = self.client.post('/administrative/production_report/', {     'beneficiary': [beneficiary.id],
                                                                                'self_seed': 1,
                                                                                'self_leaf': 3,
                                                                                'self_flour': 4,
                                                                                'days_per_month': 15
                                                                             })

        self.assertRedirects(response, '/administrative/', status_code=302, target_status_code=200, msg_prefix='', fetch_redirect_response=True)
        production_rep = ProductionReport.objects.get(beneficiary=beneficiary)
        self.assertEqual(production_rep.beneficiary, beneficiary)

    def test_new_report_complete(self):
        """
        Creating a new production report with correct information. Expecting a redirect to /administrative/
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

        self.client.login(username="user", password="testpassword")
        response = self.client.post('/administrative/production_report/', {     'beneficiary': [beneficiary.id],
                                                                                'self_seed': 1,
                                                                                'self_leaf': 3,
                                                                                'self_flour': 4,
                                                                                'days_per_month': 15,
                                                                                'exch_leaf': 5,
                                                                                'exch_sead': 7,
                                                                                'want_for_leaf': 'Efectivo',
                                                                                'want_for_seed': 'Efectivo'
                                                                             })

        self.assertRedirects(response, '/administrative/', status_code=302, target_status_code=200, msg_prefix='', fetch_redirect_response=True)
        production_rep = ProductionReport.objects.get(beneficiary=beneficiary)
        self.assertEqual(production_rep.want_for_leaf, 'Efectivo')
        self.assertEqual(production_rep.want_for_seed, 'Efectivo')

    def test_new_report_complete_as_assistant(self):
        """
        Creating a new production report with correct information. Expecting a redirect to /administrative/
        """
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
        create_user_for_group('Assistant')
        self.client.login(username="Assistant", password="testpassword")

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

        self.client.login(username="user", password="testpassword")
        response = self.client.get('/administrative/production_report/')
        self.assertEqual(response.status_code, 302)

    def test_new_report_complete_as_Field_Tech(self):
        """
        Creating a new production report with correct information. Expecting a redirect to /administrative/
        """
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
        create_user_for_group('FieldTech')
        self.client.login(username="FieldTech", password="testpassword")

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

        self.client.login(username="user", password="testpassword")
        response = self.client.get('/administrative/production_report/')
        self.assertEqual(response.status_code, 302)


    def test_new_report_complete_as_Director(self):
        """
        Creating a new production report with correct information. Expecting a redirect to /administrative/
        """
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
        create_user_for_group('Director')
        self.client.login(username="Director", password="testpassword")

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

        self.client.login(username="user", password="testpassword")
        response = self.client.get('/administrative/production_report/')
        self.assertEqual(response.status_code, 302)

class BeneficiaryTest(TestCase):
    def test_add_program_to_beneficiary(self):
        """
        Creating a new production report with correct information. Expecting a redirect to /administrative/
        """
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
        create_user_for_group('user')
        self.client.login(username="user", password="testpassword")

        program = Program.objects.create(name='Program1')
        community = Community.objects.create(
                                                name ="community1",
                                                municipality = "mun1",
                                                state = "state1"
                                            )

        response = self.client.post('/administrative/new_beneficiary/', {       'name': 'beneTest',
                                                                                'last_name_paternal': 'Test',
                                                                                'last_name_maternal': 'Test',
                                                                                'num_of_family_beneficiaries': 5,
                                                                                'contact_name': 'contactTest',
                                                                                'contact_phone': '111111',
                                                                                'account_number': '222222',
                                                                                'bank_name': 'banco',
                                                                                'promoter': [promoter.id],
                                                                                'community': [community.id],
                                                                                'member_in': [program.id],
                                                                                'curp': '123FWEDWF12',
                                                                                'house_address': 'Casa 3',
                                                                                'house_references': 'Por ahí',
                                                                                'huerto_coordinates': 'Atrás'

                                                                             })
        self.assertRedirects(response, '/administrative/beneficiaries/0', status_code=302, target_status_code=200, msg_prefix='', fetch_redirect_response=True)

        beneficiary = Beneficiary.objects.get(name='beneTest')
        self.assertEqual(beneficiary.name, 'beneTest')

        beneficiary_in_program = BeneficiaryInProgram.objects.get(beneficiary=beneficiary)
        self.assertEqual(beneficiary_in_program.program, program)

    def test_add_program_to_beneficiary_as_field_technician(self):
        """
        Creating a new production report with correct information. Expecting a redirect to /administrative/
        """
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
        create_user_for_group('FieldTech')

        self.client.login(username="FieldTech", password="testpassword")

        program = Program.objects.create(name='Program1')
        community = Community.objects.create(
                                                name ="community1",
                                                municipality = "mun1",
                                                state = "state1"
                                            )

        response = self.client.post('/administrative/new_beneficiary/', {       'name': 'beneTest',
                                                                                'last_name_paternal': 'Test',
                                                                                'last_name_maternal': 'Test',
                                                                                'num_of_family_beneficiaries': 5,
                                                                                'contact_name': 'contactTest',
                                                                                'contact_phone': '111111',
                                                                                'account_number': '222222',
                                                                                'bank_name': 'banco',
                                                                                'promoter': [promoter.id],
                                                                                'community': [community.id],
                                                                                'member_in': [program.id],
                                                                                'curp': '123FWEDWF12',
                                                                                'house_address': 'Casa 3',
                                                                                'house_references': 'Por ahí',
                                                                                'huerto_coordinates': 'Atrás'

                                                                             })
        self.assertRedirects(response, '/administrative/beneficiaries/0', status_code=302, target_status_code=200, msg_prefix='', fetch_redirect_response=True)

        beneficiary = Beneficiary.objects.get(name='beneTest')
        self.assertEqual(beneficiary.name, 'beneTest')

        beneficiary_in_program = BeneficiaryInProgram.objects.get(beneficiary=beneficiary)
        self.assertEqual(beneficiary_in_program.program, program)

    def test_add_program_to_beneficiary_as_administrative_assistant(self):
        """
        Creating a new production report with correct information. Expecting a redirect to /administrative/
        """
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
        create_user_for_group('AdministrativeAssistant')

        self.client.login(username="AdministrativeAssistant", password="testpassword")

        program = Program.objects.create(name='Program1')
        community = Community.objects.create(
                                                name ="community1",
                                                municipality = "mun1",
                                                state = "state1"
                                            )

        response = self.client.post('/administrative/new_beneficiary/', {       'name': 'beneTest',
                                                                                'last_name_paternal': 'Test',
                                                                                'last_name_maternal': 'Test',
                                                                                'num_of_family_beneficiaries': 5,
                                                                                'contact_name': 'contactTest',
                                                                                'contact_phone': '111111',
                                                                                'account_number': '222222',
                                                                                'bank_name': 'banco',
                                                                                'promoter': [promoter.id],
                                                                                'community': [community.id],
                                                                                'member_in': [program.id],
                                                                                'curp': '123FWEDWF12',
                                                                                'house_address': 'Casa 3',
                                                                                'house_references': 'Por ahí',
                                                                                'huerto_coordinates': 'Atrás'

                                                                             })
        self.assertRedirects(response, '/administrative/beneficiaries/0', status_code=302, target_status_code=200, msg_prefix='', fetch_redirect_response=True)

        beneficiary = Beneficiary.objects.get(name='beneTest')
        self.assertEqual(beneficiary.name, 'beneTest')

        beneficiary_in_program = BeneficiaryInProgram.objects.get(beneficiary=beneficiary)
        self.assertEqual(beneficiary_in_program.program, program)

    def test_add_program_to_beneficiary_as_director(self):
        """
        Creating a new production report with correct information. Expecting a redirect to /administrative/
        """
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
        create_user_for_group('Director')

        self.client.login(username="Director", password="testpassword")

        program = Program.objects.create(name='Program1')
        community = Community.objects.create(
                                                name ="community1",
                                                municipality = "mun1",
                                                state = "state1"
                                            )

        response = self.client.post('/administrative/new_beneficiary/', {       'name': 'beneTest',
                                                                                'last_name_paternal': 'Test',
                                                                                'last_name_maternal': 'Test',
                                                                                'num_of_family_beneficiaries': 5,
                                                                                'contact_name': 'contactTest',
                                                                                'contact_phone': '111111',
                                                                                'account_number': '222222',
                                                                                'bank_name': 'banco',
                                                                                'promoter': [promoter.id],
                                                                                'community': [community.id],
                                                                                'member_in': [program.id],
                                                                                'curp': '123FWEDWF12',
                                                                                'house_address': 'Casa 3',
                                                                                'house_references': 'Por ahí',
                                                                                'huerto_coordinates': 'Atrás'

                                                                             })
        self.assertRedirects(response, '/administrative/beneficiaries/0', status_code=302, target_status_code=200, msg_prefix='', fetch_redirect_response=True)

        beneficiary = Beneficiary.objects.get(name='beneTest')
        self.assertEqual(beneficiary.name, 'beneTest')

        beneficiary_in_program = BeneficiaryInProgram.objects.get(beneficiary=beneficiary)
        self.assertEqual(beneficiary_in_program.program, program)

    def test_add_multiple_programs_to_beneficiary(self):
        """
        Creating a new production report with correct information. Expecting a redirect to /administrative/
        """
        create_database()
        self.client.login(username="user", password="testpassword")

        program1 = Program.objects.create(name='Program1')

        community = Community.objects.create(
                                                name ="community1",
                                                municipality = "mun1",
                                                state = "state1"
                                            )

        response = self.client.post('/administrative/new_beneficiary/', {       'name': 'beneTest',
                                                                                'last_name_paternal': 'Test',
                                                                                'last_name_maternal': 'Test',
                                                                                'num_of_family_beneficiaries': 5,
                                                                                'contact_name': 'contactTest',
                                                                                'contact_phone': '111111',
                                                                                'account_number': '222222',
                                                                                'bank_name': 'banco',
                                                                                'promoter': [Promoter.objects.get(id=1).id],
                                                                                'community': [community.id],
                                                                                'member_in': [program1.id],
                                                                                'curp': '123FWEDWF12',
                                                                                'house_address': 'Casa 3',
                                                                                'house_references': 'Por ahí',
                                                                                'huerto_coordinates': 'Atrás'

                                                                             })
        self.assertRedirects(response, '/administrative/beneficiaries/0', status_code=302, target_status_code=200, msg_prefix='', fetch_redirect_response=True)

        beneficiary = Beneficiary.objects.get(name='beneTest')
        self.assertEqual(beneficiary.name, 'beneTest')

        beneficiary_in_program = BeneficiaryInProgram.objects.get(beneficiary=beneficiary)
        self.assertEqual(beneficiary_in_program.program, program1)

        program2 = Program.objects.create(name='Program2')

        response = self.client.post('/administrative/modify_beneficiary/', {    'beneficiary': beneficiary.id,
                                                                                'CURP': '123CURP',
                                                                                'house_address': 'Por ahí',
                                                                                'program': [program2.id]
                                                                             })
        self.assertRedirects(response, '/administrative/beneficiaries/'+str(beneficiary.id), status_code=302, target_status_code=200, msg_prefix='', fetch_redirect_response=True)

    def test_add_multiple_programs_to_beneficiary_as_field_technician(self):
        """
        Creating a new production report with correct information. Expecting a redirect to /administrative/
        """
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
        create_user_for_group('FieldTech')

        self.client.login(username="FieldTech", password="testpassword")

        program1 = Program.objects.create(name='Program1')

        community = Community.objects.create(
                                                name ="community1",
                                                municipality = "mun1",
                                                state = "state1"
                                            )

        response = self.client.post('/administrative/new_beneficiary/', {       'name': 'beneTest',
                                                                                'last_name_paternal': 'Test',
                                                                                'last_name_maternal': 'Test',
                                                                                'num_of_family_beneficiaries': 5,
                                                                                'contact_name': 'contactTest',
                                                                                'contact_phone': '111111',
                                                                                'account_number': '222222',
                                                                                'bank_name': 'banco',
                                                                                'promoter': [promoter.id],
                                                                                'community': [community.id],
                                                                                'member_in': [program1.id],
                                                                                'curp': '123FWEDWF12',
                                                                                'house_address': 'Casa 3',
                                                                                'house_references': 'Por ahí',
                                                                                'huerto_coordinates': 'Atrás'

                                                                             })
        self.assertRedirects(response, '/administrative/beneficiaries/0', status_code=302, target_status_code=200, msg_prefix='', fetch_redirect_response=True)

        beneficiary = Beneficiary.objects.get(name='beneTest')
        self.assertEqual(beneficiary.name, 'beneTest')

        beneficiary_in_program = BeneficiaryInProgram.objects.get(beneficiary=beneficiary)
        self.assertEqual(beneficiary_in_program.program, program1)

        program2 = Program.objects.create(name='Program2')

        response = self.client.post('/administrative/modify_beneficiary/', {    'beneficiary': beneficiary.id,
                                                                                'CURP': '123CURP',
                                                                                'house_address': 'Por ahí',
                                                                                'program': [program2.id]
                                                                             })
        self.assertRedirects(response, '/administrative/beneficiaries/'+str(beneficiary.id), status_code=302, target_status_code=200, msg_prefix='', fetch_redirect_response=True)


    def test_add_multiple_programs_to_beneficiary_as_administrative_assistant(self):
        """
        Creating a new production report with correct information. Expecting a redirect to /administrative/
        """
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
        create_user_for_group('AdministrativeAssistant')

        self.client.login(username="AdministrativeAssistant", password="testpassword")

        program1 = Program.objects.create(name='Program1')

        community = Community.objects.create(
                                                name ="community1",
                                                municipality = "mun1",
                                                state = "state1"
                                            )

        response = self.client.post('/administrative/new_beneficiary/', {       'name': 'beneTest',
                                                                                'last_name_paternal': 'Test',
                                                                                'last_name_maternal': 'Test',
                                                                                'num_of_family_beneficiaries': 5,
                                                                                'contact_name': 'contactTest',
                                                                                'contact_phone': '111111',
                                                                                'account_number': '222222',
                                                                                'bank_name': 'banco',
                                                                                'promoter': [promoter.id],
                                                                                'community': [community.id],
                                                                                'member_in': [program1.id],
                                                                                'curp': '123FWEDWF12',
                                                                                'house_address': 'Casa 3',
                                                                                'house_references': 'Por ahí',
                                                                                'huerto_coordinates': 'Atrás'

                                                                             })
        self.assertRedirects(response, '/administrative/beneficiaries/0', status_code=302, target_status_code=200, msg_prefix='', fetch_redirect_response=True)

    def test_pay_ok(self):
        user = create_user()
        self.client.login(username="test", password="testpassword")

        beneficiary = Beneficiary.objects.get(name='beneTest')
        self.assertEqual(beneficiary.name, 'beneTest')

        beneficiary_in_program = BeneficiaryInProgram.objects.get(beneficiary=beneficiary)
        self.assertEqual(beneficiary_in_program.program, program1)

        program2 = Program.objects.create(name='Program2')

        response = self.client.post('/administrative/modify_beneficiary/', {    'beneficiary': beneficiary.id,
                                                                                'CURP': '123CURP',
                                                                                'house_address': 'Por ahí',
                                                                                'program': [program2.id]
                                                                             })
        self.assertRedirects(response, '/administrative/beneficiaries/'+str(beneficiary.id), status_code=302, target_status_code=200, msg_prefix='', fetch_redirect_response=True)

    def test_add_multiple_programs_to_beneficiary_as_director(self):
        """
        Creating a new production report with correct information. Expecting a redirect to /administrative/
        """
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
        create_user_for_group('Director')

        self.client.login(username="Director", password="testpassword")

        program1 = Program.objects.create(name='Program1')

        community = Community.objects.create(
                                                name ="community1",
                                                municipality = "mun1",
                                                state = "state1"
                                            )

        response = self.client.post('/administrative/new_beneficiary/', {       'name': 'beneTest',
                                                                                'last_name_paternal': 'Test',
                                                                                'last_name_maternal': 'Test',
                                                                                'num_of_family_beneficiaries': 5,
                                                                                'contact_name': 'contactTest',
                                                                                'contact_phone': '111111',
                                                                                'account_number': '222222',
                                                                                'bank_name': 'banco',
                                                                                'promoter': [promoter.id],
                                                                                'community': [community.id],
                                                                                'member_in': [program1.id],
                                                                                'curp': '123FWEDWF12',
                                                                                'house_address': 'Casa 3',
                                                                                'house_references': 'Por ahí',
                                                                                'huerto_coordinates': 'Atrás'

                                                                             })
        self.assertRedirects(response, '/administrative/beneficiaries/0', status_code=302, target_status_code=200, msg_prefix='', fetch_redirect_response=True)

        beneficiary = Beneficiary.objects.get(name='beneTest')
        self.assertEqual(beneficiary.name, 'beneTest')

        beneficiary_in_program = BeneficiaryInProgram.objects.get(beneficiary=beneficiary)
        self.assertEqual(beneficiary_in_program.program, program1)

        program2 = Program.objects.create(name='Program2')

        response = self.client.post('/administrative/modify_beneficiary/', {    'beneficiary': beneficiary.id,
                                                                                'CURP': '123CURP',
                                                                                'house_address': 'Por ahí',
                                                                                'program': [program2.id]
                                                                             })
        self.assertRedirects(response, '/administrative/beneficiaries/'+str(beneficiary.id), status_code=302, target_status_code=200, msg_prefix='', fetch_redirect_response=True)

    def test_add_new_beneficiary_as_promoter(self):
        user_promoter = User.objects.create_user('promoter', 'promoter@testuser.com', 'testpassword')
        base_user_promoter = BaseUser.objects.create(user=user_promoter, name="name",
                                                        last_name_paternal="last_name_paternal",
                                                        last_name_maternal="last_name_maternal",
                                                        phone_number="phone_number",
                                                        email="email@email.com",
                                                        address="address")
        base_user_promoter.save()
        self.client.login(username="promoter", password="testpassword")
        response = self.client.get('/administrative/new_beneficiary/')
        self.assertEqual(response.status_code, 200)
        
        """
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

class TestPay(TestCase):
    def test_pay_ok(self):
        user = create_user()
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
        """
     
class NewSavingAccount(TestCase):
    def test_add_new_saving_account_assistant(self):
        """
        Creating a new sabing account. Expecting a redirect to /administrative/

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
        promoter = Promoter.objects.create(base_user=base_user_promoter,
                                            contact_name = "Contacto",
                                            contact_phone_number = "1234512312"
                                            )
        promoter.save()


        self.client.login(username="test", password="testpassword")
        beneficiary = Beneficiary.objects.create(name="Rodolfo",
                                                 last_name_paternal="Rodriguez",
                                                 last_name_maternal="Rocha",
                                                 num_of_family_beneficiaries=16,
                                                 contact_name="Juan",
                                                 contact_phone="4325671",
                                                 account_number=123456,
                                                 bank_name="Banamets",
                                                 promoter = promoter)
        beneficiary.save()
        create_user_for_group('Assistant')
        self.client.login(username="Assistant", password="testpassword")
        response = self.client.post('/administrative/new_saving_account/', {
                                                                                "name": "testAccount",
                                                                                "community": "testCommunity",
                                                                                "municipality": "testMunicipality",
                                                                                "location": "testLocation",
                                                                                "list_of_beneficiaries":[beneficiary.id],
                                                                                "total_saved_amount": 222222,
                                                                                "president_beneficiary": [beneficiary.id],
                                                                                "treasurer_beneficiary": [beneficiary.id],
                                                                                "partner_beneficiary": [beneficiary.id]
                                                                             })
        self.assertRedirects(response, '/administrative/', status_code=302, target_status_code=200, msg_prefix='', fetch_redirect_response=True)
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
        promoter = Promoter.objects.create(base_user=base_user_promoter,
                                            contact_name = "Contacto",
                                            contact_phone_number = "1234512312"
                                            )
        promoter.save()


        self.client.login(username="test", password="testpassword")
        beneficiary = Beneficiary.objects.create(name="Rodolfo",
                                                 last_name_paternal="Rodriguez",
                                                 last_name_maternal="Rocha",
                                                 num_of_family_beneficiaries=16,
                                                 contact_name="Juan",
                                                 contact_phone="4325671",
                                                 account_number=123456,
                                                 bank_name="Banamets",
                                                 promoter = promoter)
        beneficiary.save()
        create_user_for_group('Coordinator')
        self.client.login(username="Coordinator", password="testpassword")
        response = self.client.post('/administrative/new_saving_account/', {
                                                                                "name": "testAccount",
                                                                                "community": "testCommunity",
                                                                                "municipality": "testMunicipality",
                                                                                "location": "testLocation",
                                                                                "list_of_beneficiaries":[beneficiary.id],
                                                                                "total_saved_amount": 222222,
                                                                                "president_beneficiary": [beneficiary.id],
                                                                                "treasurer_beneficiary": [beneficiary.id],
                                                                                "partner_beneficiary": [beneficiary.id]
                                                                             })
        self.assertRedirects(response, '/administrative/', status_code=302, target_status_code=200, msg_prefix='', fetch_redirect_response=True)

    def test_add_new_saving_account_technician(self):
            """
            Creating a new sabing account. Expecting a redirect to /administrative/

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
            promoter = Promoter.objects.create(base_user=base_user_promoter,
                                                contact_name = "Contacto",
                                                contact_phone_number = "1234512312"
                                                )
            promoter.save()


            self.client.login(username="test", password="testpassword")
            beneficiary = Beneficiary.objects.create(name="Rodolfo",
                                                     last_name_paternal="Rodriguez",
                                                     last_name_maternal="Rocha",
                                                     num_of_family_beneficiaries=16,
                                                     contact_name="Juan",
                                                     contact_phone="4325671",
                                                     account_number=123456,
                                                     bank_name="Banamets",
                                                     promoter = promoter)
            beneficiary.save()
            create_user_for_group('Technician')
            self.client.login(username="Technician", password="testpassword")
            response = self.client.post('/administrative/new_saving_account/', {
                                                                                    "name": "testAccount",
                                                                                    "community": "testCommunity",
                                                                                    "municipality": "testMunicipality",
                                                                                    "location": "testLocation",
                                                                                    "list_of_beneficiaries":[beneficiary.id],
                                                                                    "total_saved_amount": 222222,
                                                                                    "president_beneficiary": [beneficiary.id],
                                                                                    "treasurer_beneficiary": [beneficiary.id],
                                                                                    "partner_beneficiary": [beneficiary.id]
                                                                                 })
            self.assertRedirects(response, '/administrative/', status_code=302, target_status_code=200, msg_prefix='', fetch_redirect_response=True)





