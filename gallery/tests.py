from django.test import TestCase
from django.core.files.base import ContentFile
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth.models import User, Group
from django.utils.six import BytesIO
from PIL import Image
from profiles.models import *
from gallery.models import *

def create_groups():
    group, created = Group.objects.get_or_create(name='fieldTech')
    group, created = Group.objects.get_or_create(name='promoter')
    group, created = Group.objects.get_or_create(name='owner')
    group, created = Group.objects.get_or_create(name='assistant')

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

def create_image(storage, filename, size=(100, 100), image_mode='RGB', image_format='png'):
    """
    Generate a test image, returning the filename that it was saved as.

    If ``storage`` is ``None``, the BytesIO containing the image data
    will be passed instead.
    """
    data = BytesIO()
    Image.new(image_mode, size).save(data, image_format)
    data.seek(0)
    if not storage:
        return data
    image_file = ContentFile(data.read())
    return storage.save(filename, image_file)

# Create your tests here.
class PhotoTest(TestCase):
    def test_new_photo_as_owner(self):
        """
        Adding a new photo to the gallery
        """
        user = create_user()
        create_groups()
        user.user.groups.add(Group.objects.get(name='owner'))
        c = self.client
        c.login(username="test", password="testpassword")
        image = create_image(None, 'image.png')
        image_file = SimpleUploadedFile('front.png', image.getvalue())
        response = c.post('/gallery/new_photo/', {'title': 'title', 'image': image})
        photos = Photo.objects.all()
        self.assertEqual(response.status_code, 200)

    def test_new_photo_as_fieldtech(self):
        """
        Adding a new photo to the gallery
        """
        user = create_user()
        create_groups()
        user.user.groups.add(Group.objects.get(name='fieldTech'))
        c = self.client
        c.login(username="test", password="testpassword")
        image = Image.open('gallery/images/mta_logo.png')
        response = c.post('/gallery/new_photo/', {'title': 'title', 'image': image})
        photos = Photo.objects.all()
        self.assertEqual(len(photos), 1)
        self.assertEqual(response.status_code, 200)

    def test_new_photo_as_assistant(self):
        """
        Adding a new photo to the gallery
        """
        user = create_user()
        create_groups()
        user.user.groups.add(Group.objects.get(name='assistant'))
        c = self.client
        c.login(username="test", password="testpassword")
        image = Image.open('gallery/images/mta_logo.png')
        response = c.post('/gallery/new_photo/', {'title': '', 'image': image})
        photos = Photo.objects.all()
        self.assertEqual(len(photos), 1)
        self.assertEqual(response.status_code, 200)

    def test_new_photo_as_promoter(self):
        """
        Adding a new photo to the gallery
        """
        #user = User.objects.create_user('test2', 'test2@testuser.com', 'testpassword')
        promoter = create_promoter()
        create_groups()
        promoter.base_user.user.groups.add(Group.objects.get(name='promoter'))
        c = self.client
        c.login(username="test", password="testpassword")
        image = Image.open('gallery/images/mta_logo.png')
        response = c.post('/gallery/new_photo/', {'title': 'title', 'image': image})
        photos = Photo.objects.all()
        self.assertEqual(len(photos), 0)
        self.assertEqual(response.status_code, 200)

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
