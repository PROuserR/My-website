from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Task(models.Model):
    title = models.CharField(max_length=200)
    note = models.TextField(default='None')
    finished = models.BooleanField(default=False)
    date_added = models.DateTimeField(auto_now_add=True)
    high_priority = models.BooleanField(default=False)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    

    def __str__(self):
    #To return the text representation of the model
        return self.title


class WeeklyTask(models.Model):
    title = models.CharField(max_length=200)
    note = models.TextField(default='None')
    finished = models.BooleanField(default=False)
    high_priority = models.BooleanField(default=False)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    day = models.CharField(max_length=20)
    hour = models.CharField(max_length=20)


    def __str__(self):
    #To return the text representation of the model
        return self.title