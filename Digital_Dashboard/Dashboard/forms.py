from django.forms import ModelForm
from django import forms
from django.forms.widgets import Widget
from .models import Districts

#Widgets is using boostrap styling

class DistrictForm(ModelForm):
    class Meta:
        model = Districts
        fields = ['state', 'district_id']

        widgets = {
            'state' : forms.TextInput(attrs={'class' : 'form-control', 'style': 'width: 150px;'}),
            'district_id' : forms.TextInput(attrs={'class' : 'form-control', 'style': 'width: 150px;'}),

        }