from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Project(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    rules = models.TextField()
    admin = models.ForeignKey(User, on_delete=models.CASCADE, related_name='admin')
    date_started = models.DateTimeField(auto_now_add=True)
    date_to_be_finished = models.DateTimeField()
    tasks = models.TextField(blank=True)
    members = models.TextField(blank=True)
    finished = models.BooleanField(default=False)

    def __str__(self):
        return self.name