from django.contrib import admin

# Register your models here.
from .models import Task, WeeklyTask

admin.site.register(Task)
admin.site.register(WeeklyTask)