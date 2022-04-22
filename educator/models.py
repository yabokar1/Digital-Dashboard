import uuid

from django.db import models
from django.contrib.auth.models import User
# Create your models here.
from django.db.models.signals import post_save,post_delete



class EducatorProfile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,null=True,
                                blank=True)
    name = models.CharField(max_length=200,blank=True,null=True)
    email = models.EmailField(max_length=500,blank=True,null=True)
    id = models.UUIDField(default=uuid.uuid4,unique=True,primary_key=True,editable=False)



    def __str__(self):
        return str(self.user.username)


def educatorUpdated(sender,instance,created,**kwargs):
    print('Profile Saved!')
    print('Instance:',instance)
    print('CREATED',created)

def deleteEducator(sender,instance,**kwargs):
    print('Deleting user..')

post_save.connect(educatorUpdated,sender=EducatorProfile)
post_delete.connect(deleteEducator,sender=EducatorProfile)