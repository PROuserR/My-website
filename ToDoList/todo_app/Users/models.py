from django.db import models
from django.contrib.auth.models import User


accounts = [(None, 'None'),
            ('google', 'Google'),
            ('github', 'Github')]

# Create your models here.
class Profile(models.Model):
    profile_pic = models.ImageField(upload_to="img/", blank=True)
    owner = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.owner