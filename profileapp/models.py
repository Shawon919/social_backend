from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class UserProfile(models.Model):
    profile = models.OneToOneField(User,on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='photos/',null=True)
    address = models.CharField(max_length=100,blank=True)
    bio = models.TextField(max_length=2000,blank=True)
    is_avtive = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.address}'
    



class ChageProfile(models.Model):
     profile = models.ForeignKey(UserProfile,on_delete=models.CASCADE)
     new_photo = models.ImageField(upload_to='profile/')
     caption = models.TextField(max_length=600)
     

     def __str__(self):
        return f'{self.pk}'
     

