from django import forms
from.models import *
from profiles.models import *

class PhotoForm(forms.ModelForm):
    image = forms.ImageField(required=True)
    class Meta:
        model = Photo
        fields = ['title',
                  'description',
                  'image']
