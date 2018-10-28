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
