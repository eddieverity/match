from django import forms
from .models import *

class ImageUploadForm(forms.ModelForm):
    class Meta:
        model = Images
        fields = ('user_pic',)