from django.db.models.signals import pre_save
from .models import *



def updateStudent(sender, instance, **kwargs):
    print('Signal Triggered')


pre_save.connect(updateStudent, sender=Students)