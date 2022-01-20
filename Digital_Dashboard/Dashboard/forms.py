from django.forms import ModelForm
from django import forms
from django.forms.widgets import Widget
from django.contrib.auth.forms import UserCreationForm
from django.db import models
from django.contrib.auth.models import User
from .models import Districts, UserProfile

#Widgets is using bootsrap styling

USER_TYPES= [
    ('student', 'Student'),
    ('educator', 'Educator'),
    ('policymaker', 'PolicyMaker'),
    ]


COUNTRIES= [
    ('canada', 'Canada'),
    ('usa', 'USA')
]

STATES = [
    ('utah', 'Utah'),
    ('illinois', 'Ilinois'),
    ('north carolina', 'North Carolina'),
    ('missouri', 'Missouri'),
    ('washington', 'Washington')
]
    # states = ['Utah', 'Illinois', 'Wisconsin', 'NC', 'Missouri', 'Washington', 'Connecticut', 'Massachusetts', 'NY', 'Indiana', 'Virginia', 'Ohio', 'New Jersey', 'California', 'DOC', 'Arizona','Texas']


class DistrictForm(ModelForm):
    class Meta:
        model = Districts
        fields = ['state', 'district_id']

        widgets = {
            'state' : forms.TextInput(attrs={'class' : 'form-control', 'style': 'width: 150px;'}),
            'district_id' : forms.TextInput(attrs={'class' : 'form-control', 'style': 'width: 150px;'}),

        }

class UserForm(UserCreationForm):
    first_name = forms.CharField()
    last_name = forms.CharField()
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ('first_name','last_name','username', 'email', 'password1' ,'password2' )


class ProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('user_type',)

        widgets = {
            'user_type': forms.Select(choices=USER_TYPES)
            
        }


class FilterForm(forms.Form):
    country = forms.CharField(widget=forms.Select(choices=COUNTRIES, attrs={'onchange': 'form.submit();'}))
    # state = forms.CharField(label="State/Province", widget=forms.Select(choices=STATES))






