from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Blog(models.Model):
    text = models.CharField(max_length=200)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text


class Entry(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    text = models.TextField()
    image = models.ImageField(blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Entries'

    def __str__(self):
        return self.text


class Comment(models.Model):
    text = models.TextField()
    entry = models.ForeignKey(Entry, on_delete=models.CASCADE)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text