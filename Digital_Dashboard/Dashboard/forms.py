from django.forms import ModelForm
from django import forms
from django.forms.widgets import Widget
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Districts

#Widgets is using bootsrap styling

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
        fields = ('first_name','last_name', 'username', 'email', 'password1' ,'password2' )
