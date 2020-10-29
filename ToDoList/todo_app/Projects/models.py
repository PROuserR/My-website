from django.db import models
from django.contrib.auth.models import User


data_types = [('linear', 'Linear'),
              ('tree', 'Tree'),]


class Tree:
    root = ''
    nodes = []

# Create your models here.
class Project(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    rules = models.TextField()
    admin = models.ForeignKey(User, on_delete=models.CASCADE, related_name='admin')
    date_started = models.DateTimeField(auto_now_add=True)
    date_to_be_finished = models.DateTimeField()
    tasks = models.TextField(null=True, unique=True,)
    members = models.TextField(null=True, unique=True)
    finished = models.BooleanField(default=False)
    type = models.CharField(max_length=20, choices=data_types, default='Linear')
    def __str__(self):
        return self.name


class TreeField(models.Model):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    project = models.ForeignKey(Project, on_delete=models.CASCADE)