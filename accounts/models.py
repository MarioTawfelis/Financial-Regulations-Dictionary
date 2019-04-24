from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save


# Profile model for Users to store personal information
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    job_title = models.CharField(max_length=500, blank=True)
    company = models.CharField(max_length=500, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    image = models.ImageField(upload_to='profile_pictures', null=True)

    def __str__(self):
        return self.user.username


""" Title: How to Extend Django User Model
Author: Vitor Freitas
Date: Jul 22, 2016
Availability: https://simpleisbetterthancomplex.com/tutorial/2016/07/22/how-to-extend-django-user-model.html """


def create_profile(sender, **kwargs):
    if kwargs['created']:
        Profile.objects.create(user=kwargs['instance'])


post_save.connect(create_profile, sender=User)
