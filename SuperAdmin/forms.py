from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from django.conf import settings
from django.forms import ValidationError
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model

from .models import Ministry, District, PoliceStation

User = get_user_model()


class MinistryForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(MinistryForm, self).__init__(*args, **kwargs)
        for MinistryName in self.fields.keys():
            self.fields[MinistryName].widget.attrs.update({
                'class': 'form-control',
            })

    class Meta:
        model = Ministry
        fields = ['ministry_name', 'minister_name', 'email']


class GovtSignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'ministry_name', 'password1', 'password2']

    email = forms.EmailField(label=_('Email'), help_text=_('Required. Enter an existing email address.'))

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_ministry_incharge = True
        if commit:
            user.save()
        return user

    def clean_email(self):
        email = self.cleaned_data['email']

        user = User.objects.filter(email__iexact=email).exists()
        if user:
            raise ValidationError(_('You can not use this email address.'))

        return email


class GovtSignUpUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'ministry_name']


class UnoSignUpUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'district', 'police_station', 'first_name', 'last_name', 'email', 'ministry_name']


class DistrictForm(forms.ModelForm):
    class Meta:
        model = District
        fields = ['district']


class PoliceStationForm(forms.ModelForm):
    class Meta:
        model = PoliceStation
        fields = ['district', 'police_station', 'email']


class UNOSignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'district', 'police_station', 'email', 'ministry_name', 'password1', 'password2']

    email = forms.EmailField(label=_('Email'), help_text=_('Required. Enter an existing email address.'))

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_uno = True
        if commit:
            user.save()
        return user

    def clean_email(self):
        email = self.cleaned_data['email']

        user = User.objects.filter(email__iexact=email).exists()
        if user:
            raise ValidationError(_('You can not use this email address.'))

        return email

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['police_station'].queryset = PoliceStation.objects.none()

        if 'district' in self.data:
            try:
                district_id = int(self.data.get('district'))
                self.fields['police_station'].queryset = PoliceStation.objects.filter(district_id=district_id).order_by('police_station')
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty Police_station queryset
        elif self.instance.pk:
            self.fields['police_station'].queryset = self.instance.district.police_station_set.order_by('police_station')

