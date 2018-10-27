from django.db import models

# Create your models here.
class Photo(models.Model):
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=250, blank=True)
    image = models.ImageField(upload_to = 'gallery/images/')

    def __str__(self):
        return self.title
