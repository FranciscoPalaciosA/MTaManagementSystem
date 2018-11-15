from django.db import models
from django.utils import timezone

# Create your models here.
class Photo(models.Model):
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=250, blank=True)
    image = models.ImageField(upload_to = 'gallery/images/')
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title

class Video(models.Model):
    title = models.CharField(max_length=50)
    link = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title
