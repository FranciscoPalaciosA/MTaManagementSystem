from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User, Group
from profiles.models import *
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

def create_all_groups():
    group, created = Group.objects.get_or_create(name='Promoter')
    group, created = Group.objects.get_or_create(name='Asistente Administrativo')
    group, created = Group.objects.get_or_create(name='Coordinador Administrativo')
    group, created = Group.objects.get_or_create(name='Director')
    group, created = Group.objects.get_or_create(name='Técnico de Campo')
    group, created = Group.objects.get_or_create(name='Capacitador')
    group, created = Group.objects.get_or_create(name='Contador')


class ContactTest(TestCase):
    def test_delete_contact_as_director(self):
        """
        Test to delete a contact as director
        Expected a redirect to /directory/
        Expected the contact eliminated
        """
        user = User.objects.create_user('user', 'user@testuser.com', 'testpassword')
        base_user = BaseUser.objects.create(user=user, name="name",
                                            last_name_paternal="last_name_paternal",
                                            last_name_maternal="last_name_maternal",
                                            phone_number="phone_number",
                                            email="email@email.com",
                                            address="address")
        base_user.save()
        create_all_groups()
        user.groups.add(Group.objects.get(name='Director'))
        self.client.login(username="user", password="testpassword")
        contact = Contact.objects.create(first_name="contact",
                                        last_name_paternal="Test",
                                        last_name_maternal="Test",
                                        phone_number="123456",
                                        email="contact@test.com",
                                        contact_type="Volunteer",
                                        institution="INEGI",
                                        comments="test")
        contact.save()
        self.assertEquals(contact.deleted_at, None)
        contactId = contact.id
        response = self.client.get('/directory/delete_contact/'+str(contactId))
        self.assertRedirects(response, '/directory/', status_code=302, target_status_code=200, msg_prefix='', fetch_redirect_response=True)
        deletedContact = Contact.objects.get(id=contactId)
        self.assertNotEqual(deletedContact.deleted_at, None)

    def test_delete_contact_as_adminAssisant(self):
        """
        Test to delete a contact as adminAssistan
        Expected a redirect to /directory/
        Expected the contact not eliminated
        """
        user = User.objects.create_user('user', 'user@testuser.com', 'testpassword')
        base_user = BaseUser.objects.create(user=user, name="name",
                                            last_name_paternal="last_name_paternal",
                                            last_name_maternal="last_name_maternal",
                                            phone_number="phone_number",
                                            email="email@email.com",
                                            address="address")
        base_user.save()
        create_all_groups()
        user.groups.add(Group.objects.get(name='Asistente Administrativo'))
        self.client.login(username="user", password="testpassword")
        contact = Contact.objects.create(first_name="contact",
                                        last_name_paternal="Test",
                                        last_name_maternal="Test",
                                        phone_number="123456",
                                        email="contact@test.com",
                                        contact_type="Volunteer",
                                        institution="INEGI",
                                        comments="test")
        contact.save()
        self.assertEquals(contact.deleted_at, None)
        contactId = contact.id
        response = self.client.get('/directory/delete_contact/'+str(contactId))
        self.assertRedirects(response, '/directory/', status_code=302, target_status_code=200, msg_prefix='', fetch_redirect_response=True)
        deletedContact = Contact.objects.get(id=contactId)
        self.assertEquals(deletedContact.deleted_at, None)

    def test_delete_contact_as_adminCoord(self):
        """
        Test to delete a contact as adminisitrative coordinator
        Expected a redirect to /directory/
        Expected the contact not eliminated
        """
        user = User.objects.create_user('user', 'user@testuser.com', 'testpassword')
        base_user = BaseUser.objects.create(user=user, name="name",
                                            last_name_paternal="last_name_paternal",
                                            last_name_maternal="last_name_maternal",
                                            phone_number="phone_number",
                                            email="email@email.com",
                                            address="address")
        base_user.save()
        create_all_groups()
        user.groups.add(Group.objects.get(name='Coordinador Administrativo'))
        self.client.login(username="user", password="testpassword")
        contact = Contact.objects.create(first_name="contact",
                                        last_name_paternal="Test",
                                        last_name_maternal="Test",
                                        phone_number="123456",
                                        email="contact@test.com",
                                        contact_type="Volunteer",
                                        institution="INEGI",
                                        comments="test")
        contact.save()
        self.assertEquals(contact.deleted_at, None)
        contactId = contact.id
        response = self.client.get('/directory/delete_contact/'+str(contactId))
        self.assertRedirects(response, '/directory/', status_code=302, target_status_code=200, msg_prefix='', fetch_redirect_response=True)
        deletedContact = Contact.objects.get(id=contactId)
        self.assertEquals(deletedContact.deleted_at, None)

    def test_delete_contact_as_fieldTech(self):
        """
        Test to delete a contact as field Technician
        Expected a redirect to /directory/
        Expected the contact not eliminated
        """
        user = User.objects.create_user('user', 'user@testuser.com', 'testpassword')
        base_user = BaseUser.objects.create(user=user, name="name",
                                            last_name_paternal="last_name_paternal",
                                            last_name_maternal="last_name_maternal",
                                            phone_number="phone_number",
                                            email="email@email.com",
                                            address="address")
        base_user.save()
        create_all_groups()
        user.groups.add(Group.objects.get(name='Técnico de Campo'))
        self.client.login(username="user", password="testpassword")
        contact = Contact.objects.create(first_name="contact",
                                        last_name_paternal="Test",
                                        last_name_maternal="Test",
                                        phone_number="123456",
                                        email="contact@test.com",
                                        contact_type="Volunteer",
                                        institution="INEGI",
                                        comments="test")
        contact.save()
        self.assertEquals(contact.deleted_at, None)
        contactId = contact.id
        response = self.client.get('/directory/delete_contact/'+str(contactId))
        self.assertRedirects(response, '/directory/', status_code=302, target_status_code=200, msg_prefix='', fetch_redirect_response=True)
        deletedContact = Contact.objects.get(id=contactId)
        self.assertEquals(deletedContact.deleted_at, None)

    def test_delete_contact_as_accountant(self):
        """
        Test to delete a contact as accountant
        Expected a redirect to /directory/
        Expected the contact not eliminated
        """
        user = User.objects.create_user('user', 'user@testuser.com', 'testpassword')
        base_user = BaseUser.objects.create(user=user, name="name",
                                            last_name_paternal="last_name_paternal",
                                            last_name_maternal="last_name_maternal",
                                            phone_number="phone_number",
                                            email="email@email.com",
                                            address="address")
        base_user.save()
        create_all_groups()
        user.groups.add(Group.objects.get(name='Contador'))
        self.client.login(username="user", password="testpassword")
        contact = Contact.objects.create(first_name="contact",
                                        last_name_paternal="Test",
                                        last_name_maternal="Test",
                                        phone_number="123456",
                                        email="contact@test.com",
                                        contact_type="Volunteer",
                                        institution="INEGI",
                                        comments="test")
        contact.save()
        self.assertEquals(contact.deleted_at, None)
        contactId = contact.id
        response = self.client.get('/directory/delete_contact/'+str(contactId))
        self.assertRedirects(response, '/directory/', status_code=302, target_status_code=200, msg_prefix='', fetch_redirect_response=True)
        deletedContact = Contact.objects.get(id=contactId)
        self.assertEquals(deletedContact.deleted_at, None)


    def test_delete_contact_as_trainer(self):
        """
        Test to delete a contact as trainer
        Expected a redirect to /directory/
        Expected the contact not eliminated
        """
        user = User.objects.create_user('user', 'user@testuser.com', 'testpassword')
        base_user = BaseUser.objects.create(user=user, name="name",
                                            last_name_paternal="last_name_paternal",
                                            last_name_maternal="last_name_maternal",
                                            phone_number="phone_number",
                                            email="email@email.com",
                                            address="address")
        base_user.save()
        create_all_groups()
        user.groups.add(Group.objects.get(name='Capacitador'))
        self.client.login(username="user", password="testpassword")
        contact = Contact.objects.create(first_name="contact",
                                        last_name_paternal="Test",
                                        last_name_maternal="Test",
                                        phone_number="123456",
                                        email="contact@test.com",
                                        contact_type="Volunteer",
                                        institution="INEGI",
                                        comments="test")
        contact.save()
        self.assertEquals(contact.deleted_at, None)
        contactId = contact.id
        response = self.client.get('/directory/delete_contact/'+str(contactId))
        self.assertRedirects(response, '/directory/', status_code=302, target_status_code=200, msg_prefix='', fetch_redirect_response=True)
        deletedContact = Contact.objects.get(id=contactId)
        self.assertEquals(deletedContact.deleted_at, None)


class AddContactTest(TestCase):
    def test_table_Contact_only_selfconsumption(self):
        """
        Testing model Contact. Expecting assertEqual in all fields
        """
        contact = Contact.objects.create(first_name="contact",
                                        last_name_paternal="Test",
                                        last_name_maternal="Test",
                                        phone_number="123456",
                                        email="contact@test.com",
                                        contact_type="Volunteer",
                                        institution="INEGI",
                                        comments="test")
        contact.save()
        new_contact1 = Contact.objects.get(email="contact@test.com")
        self.assertEqual(new_contact1.first_name, 'contact')
        self.assertEqual(new_contact1.last_name_paternal, 'Test')
        self.assertEqual(new_contact1.last_name_maternal, 'Test')
        self.assertEqual(new_contact1.contact_type, 'Volunteer')
        self.assertEqual(new_contact1.institution, 'INEGI')
        self.assertEqual(new_contact1.comments, 'test')

    def test_new_contact_only_selfconsumption(self):
        """
        Testing form in new_contact. Expecting a redirect to /directory/
        """
        user = create_user()
        self.client.login(username="test", password="testpassword")
        response = self.client.post('/directory/new_contact/', {'first_name': 'contact',
                                                                                'last_name_paternal': 'Test2',
                                                                                'last_name_maternal': 'Test2',
                                                                                'phone_number': '1234567',
                                                                                'email': 'contact2@test.com',
                                                                                'contact_type': 'Volunteer',
                                                                                'institution': 'INEGI',
                                                                                'comments': 'test'
                                                                             })
        #print("\n\n\n\n"+response)

        self.assertRedirects(response, '/directory/', status_code=302, target_status_code=200, msg_prefix='', fetch_redirect_response=True)
        new_contact = Contact.objects.get(email="contact2@test.com")
        self.assertEqual(new_contact.first_name, 'contact')
        self.assertEqual(new_contact.last_name_paternal, 'Test2')
        self.assertEqual(new_contact.last_name_maternal, 'Test2')
        self.assertEqual(new_contact.contact_type, 'Volunteer')
        self.assertEqual(new_contact.institution, 'INEGI')
        self.assertEqual(new_contact.comments, 'test')

class AddInstitutionTest(TestCase):
    def test_model_Institution_only_selfconsumption(self):
        institution = Institution.objects.create(name="Test1",
                                         type_of_institution="Education",
                                         comments="test"
                                        )
        institution.save()
        new_institution = Institution.objects.get(name="Test1")
        self.assertEqual(new_institution.type_of_institution, 'Education')
        self.assertEqual(new_institution.comments, 'test')

    def test_new_institution_only_selfconsumption(self):
        """
        Creating a new institution with correct information. Expecting a redirect to /directory/
        """
        user = create_user()
        self.client.login(username="test", password="testpassword")
        response = self.client.post('/directory/new_institution/', {'name': 'Test',
                                                                    'type_of_institution': 'Education',
                                                                    'comments': 'test'
                                                                    })
        #print("\n\n\n\n"+response)
        self.assertRedirects(response, '/directory/', status_code=302, target_status_code=200, msg_prefix='', fetch_redirect_response=True)
        new_institution = Institution.objects.get(name="Test")
        self.assertEqual(new_institution.type_of_institution, 'Education')
        self.assertEqual(new_institution.comments, 'test')

class InstitutionDirectoryTest(TestCase):
    def test_new_institution_directory(self):
        institution = Institution.objects.create(name="Test1",
                                         type_of_institution="Other",
                                         comments="test"
                                        )
        institution.save()
        new_institution = Institution.objects.get(name="Test1")
        self.assertEqual(new_institution.type_of_institution, 'Other')
        self.assertEqual(new_institution.comments, 'test')
        user = create_user()
        self.client.login(username="test", password="testpassword")
        response = self.client.get('/directory/institution_directory/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test1')
