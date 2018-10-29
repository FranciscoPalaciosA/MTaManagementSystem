from django import forms
from.models import *
from profiles.models import *

class PhotoForm(forms.ModelForm):
    image = forms.ImageField(required=False)
    class Meta:
        model = Photo
        fields = ['title',
                  'description',
                  'image']
