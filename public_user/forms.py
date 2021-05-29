from django import forms
from .models import *


class ComplaintForms(forms.ModelForm):

    class Meta:
        model = Complaint
        fields = ['district', 'police_station', 'location', 'image', 'note']
        # fields = ['location', 'image', 'note']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['police_station'].queryset = PoliceStation.objects.none()

        if 'district' in self.data:
            try:
                district_id = int(self.data.get('district'))
                self.fields['police_station'].queryset = PoliceStation.objects.filter(district_id=district_id).order_by('police_station')
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty City queryset
        elif self.instance.pk:
            self.fields['police_station'].queryset = self.instance.district.police_station_set.order_by('police_station')


class ComplaintNextStepsForms(forms.Form):
    email_or_start_date = forms.CharField()
