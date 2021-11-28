from django.forms import ModelForm
from .models import Districts


class DistrictForm(ModelForm):
    class Meta:
        model = Districts
        fields = ['state', 'district_id']
