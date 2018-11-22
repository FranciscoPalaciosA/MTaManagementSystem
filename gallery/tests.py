from django.test import TestCase
from django.core.files.base import ContentFile
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth.models import User, Group
from django.utils.six import BytesIO
# from io import BytesIO
from PIL import Image
import os
from django.core.files import File
from profiles.models import *
from gallery.models import *

def create_groups():
    group, created = Group.objects.get_or_create(name='Promoter')
    group, created = Group.objects.get_or_create(name='Asistente Administrativo')
    group, created = Group.objects.get_or_create(name='Coordinador Administrativo')
    group, created = Group.objects.get_or_create(name='Director')
    group, created = Group.objects.get_or_create(name='Técnico de Campo')
    group, created = Group.objects.get_or_create(name='Capacitador')

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
    community = Community.objects.create(
                                            name='name',
                                            municipality='municipality',
                                            state='state'
                                        )
    user = User.objects.create_user('promoter', 'promoter@testuser.com', 'testpassword')
    base_user = BaseUser.objects.create(user=user, name="name",
                                        last_name_paternal="last_name_paternal",
                                        last_name_maternal="last_name_maternal",
                                        phone_number="phone_number",
                                        email="email@email.com",
                                        address="address")
    base_user.save()
    promoter = Promoter.objects.create(base_user=base_user,
                                        contact_name = "Contacto",
                                        contact_phone_number = "1234512312"
                                        )
    beneficiary = Beneficiary.objects.create(id=1,
                                             name="Rodolfo",
                                             last_name_paternal="Rodriguez",
                                             last_name_maternal="Rocha",
                                             community= community,
                                             num_of_family_beneficiaries=16,
                                             promoter=promoter,
                                             contact_name="Juan",
                                             contact_phone="4424325671",
                                             account_number=123456,
                                             bank_name="Banamets")
    beneficiary.save()
    return beneficiary


# Create your tests here.
class PhotoTest(TestCase):
    # Add new photos
    def test_new_photo_as_director(self):
        """
        Adding a new photo to the gallery
        """
        user = create_user()
        create_groups()
        user.user.groups.add(Group.objects.get(name='Director'))
        c = self.client
        c.login(username="test", password="testpassword")
        image = open('gallery/images/mta_logo.png', 'rb')
        response = c.post('/gallery/new_photo/', {'title': 'title', 'image': image})
        photos = Photo.objects.all()
        self.assertEqual(len(photos), 0)
        self.assertEqual(response.status_code, 302)

    def test_new_photo_as_fieldtech(self):
        """
        Adding a new photo to the gallery
        """
        user = create_user()
        create_groups()
        user.user.groups.add(Group.objects.get(name='Técnico de Campo'))
        c = self.client
        c.login(username="test", password="testpassword")
        img = open('gallery/images/mta_logo.png', 'rb')
        # image = open('gallery/images/nimage.docx', 'rb')
        response = c.post('/gallery/new_photo/', {'title': 'title', 'image': img})
        photos = Photo.objects.all()
        self.assertEqual(len(photos), 1)
        self.assertEqual(response.status_code, 302)

    def test_new_photo_as_administrative_assistant(self):
        """
        Adding a new photo to the gallery
        """
        user = create_user()
        create_groups()
        user.user.groups.add(Group.objects.get(name='Asistente Administrativo'))
        c = self.client
        c.login(username="test", password="testpassword")
        image = open('gallery/images/mta_logo.png', 'rb')
        # image = open('gallery/images/nimage.docx', 'rb')
        response = c.post('/gallery/new_photo/', {'title': 'title', 'image': image})
        photos = Photo.objects.all()
        self.assertEqual(len(photos), 1)
        self.assertEqual(response.status_code, 302)

    def test_new_photo_as_administrative_coordinator(self):
        """
        Adding a new photo to the gallery
        """
        user = create_user()
        create_groups()
        user.user.groups.add(Group.objects.get(name='Coordinador Administrativo'))
        c = self.client
        c.login(username="test", password="testpassword")
        # image = open('gallery/images/mta_logo.png', 'rb')
        image = open('gallery/images/nimage.docx', 'rb')
        response = c.post('/gallery/new_photo/', {'title': 'title', 'image': image})
        photos = Photo.objects.all()
        self.assertEqual(len(photos), 1)
        self.assertEqual(response.status_code, 302)

    def test_new_photo_as_promoter(self):
        """
        Adding a new photo to the gallery
        """
        # promoter = create_promoter()
        # create_groups()
        user = create_user()
        create_groups()
        user.user.groups.add(Group.objects.get(name='Coordinador Administrativo'))
        # promoter.base_user.user.groups.add(Group.objects.get(name='Promoter'))
        c = self.client
        c.login(username="test", password="testpassword")
        image = open('gallery/images/mta_logo.png', 'rb')
        response = c.post('/gallery/new_photo/', {'title': 'title', 'image': image})
        photos = Photo.objects.all()
        self.assertEqual(len(photos), 0)
        self.assertEqual(response.status_code, 302)

    # View photo gallery
    def test_view_gallery_as_director(self):
        """
        Accessing the gallery index to view images as a director
        """
        # Create user and login
        user = create_user()
        create_groups()
        user.user.groups.add(Group.objects.get(name='Director'))
        self.client.login(username="test", password="testpassword")
        photo = Photo.objects.create(
                                        title="new title",
                                        description="new description",
                                        image='gallery/images/mta_logo.png'
                                    )
        photo.save()
        # Assert the template contains the photo
        response = self.client.get('/gallery/')
        self.assertContains(response, photo.image.url)

    def test_view_gallery_as_fieldtech(self):
        """
        Accessing the gallery index to view images as a director
        """
        # Create user and login
        user = create_user()
        create_groups()
        user.user.groups.add(Group.objects.get(name='Técnico de Campo'))
        self.client.login(username="test", password="testpassword")
        photo = Photo.objects.create(
                                        title="new title",
                                        description="new description",
                                        image='gallery/images/mta_logo.png'
                                    )
        photo.save()
        # Assert the template contains the photo
        response = self.client.get('/gallery/')
        self.assertContains(response,photo.image.url)

    def test_view_gallery_as_administrative_assistant(self):
        """
        Accessing the gallery index to view images as a director
        """
        # Create user and login
        user = create_user()
        create_groups()
        user.user.groups.add(Group.objects.get(name='Asistente Administrativo'))
        self.client.login(username="test", password="testpassword")
        photo = Photo.objects.create(
                                        title="new title",
                                        description="new description",
                                        image='gallery/images/mta_logo.png'
                                    )
        photo.save()
        # Assert the template contains the photo
        response = self.client.get('/gallery/')
        self.assertContains(response, photo.image.url)

    def test_view_gallery_as_administrative_coordinator(self):
        """
        Accessing the gallery index to view images as a director
        """
        # Create user and login
        user = create_user()
        create_groups()
        user.user.groups.add(Group.objects.get(name='Coordinador Administrativo'))
        self.client.login(username="test", password="testpassword")
        photo = Photo.objects.create(
                                        title="new title",
                                        description="new description",
                                        image='gallery/images/mta_logo.png'
                                    )
        photo.save()
        # Assert the template contains the photo
        response = self.client.get('/gallery/')
        self.assertContains(response, photo.image.url)

    def test_view_gallery_as_promoter(self):
        """
        Accessing the gallery index to view images as a director
        """
        # Create user and login
        promoter = create_promoter()
        create_groups()
        promoter.base_user.user.groups.add(Group.objects.get(name='Promoter'))
        self.client.login(username="test", password="testpassword")
        # Assert the template contains the photo
        response = self.client.get('/gallery/')
        self.assertRedirects(response, '/administrative/', status_code=302, target_status_code=200)

class VideoTest(TestCase):
    def test_new_video_as_administrative_assistant(self):
        """
        Adding a new video to the gallery as Administrative Assistant
        """
        user = create_user()
        group, created = Group.objects.get_or_create(name='Asistente Administrativo')
        user.user.groups.add(group)
        c = self.client
        c.login(username="test", password="testpassword")
        response = c.post('/gallery/new_video/', {  'title': 'video',
                                                    'link': 'https://www.youtube.com/watch?v=cYlB3dN-udY'})

        self.assertRedirects(response, '/gallery/', status_code=302, target_status_code=200, msg_prefix='', fetch_redirect_response=True)
        video = Video.objects.get(title='video')
        self.assertEqual(video.link, 'https://www.youtube.com/watch?v=cYlB3dN-udY')

    def test_new_video_as_administrative_coordinator(self):
        """
        Adding a new video to the gallery as Administrative coordinator
        """
        user = create_user()
        group, created = Group.objects.get_or_create(name='Coordinador Administrativo')
        user.user.groups.add(group)
        c = self.client
        c.login(username="test", password="testpassword")
        response = c.post('/gallery/new_video/', {  'title': 'video',
                                                    'link': 'https://www.youtube.com/watch?v=cYlB3dN-udY'})

        self.assertRedirects(response, '/gallery/', status_code=302, target_status_code=200, msg_prefix='', fetch_redirect_response=True)
        video = Video.objects.get(title='video')
        self.assertEqual(video.link, 'https://www.youtube.com/watch?v=cYlB3dN-udY')

    def test_new_video_as_field_technician(self):
        """
        Adding a new video to the gallery as Field Technician
        """
        user = create_user()
        group, created = Group.objects.get_or_create(name='Técnico de Campo')
        user.user.groups.add(group)
        c = self.client
        c.login(username="test", password="testpassword")
        response = c.post('/gallery/new_video/', {  'title': 'video',
                                                    'link': 'https://www.youtube.com/watch?v=cYlB3dN-udY'})

        self.assertRedirects(response, '/gallery/', status_code=302, target_status_code=200, msg_prefix='', fetch_redirect_response=True)
        video = Video.objects.get(title='video')
        self.assertEqual(video.link, 'https://www.youtube.com/watch?v=cYlB3dN-udY')
