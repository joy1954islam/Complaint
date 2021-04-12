from django import forms
from .models import *


class ComplaintForms(forms.ModelForm):
    ministry_name = forms.CharField(disabled=True)

    class Meta:
        model = Complaint
        fields = ['ministry_name', 'location', 'image', 'note']
