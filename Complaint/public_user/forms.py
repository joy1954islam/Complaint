from django import forms
from .models import *


class ComplaintForms(forms.ModelForm):
    class Meta:
        model = Complaint
        fields = ['location', 'image', 'note']
