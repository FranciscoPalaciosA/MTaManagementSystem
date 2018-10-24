from django.test import TestCase
from django.contrib.auth.models import User
from PIL import Image

# Create your tests here.
class PhotoTest(TestCase):
    def test_new_photo(self):
        """
        Adding a new photo to the gallery
        """
        user = User.objects.create_user('test2', 'test2@testuser.com', 'testpassword')
        c = self.client
        c.login(username="test2", password="testpassword")
        image = Image.open('gallery/images/mta_logo.png')
        response = c.post('/gallery/new_photo/', {'title': 'title', 'image': image})

        self.assertEqual(response.status_code, 200)
