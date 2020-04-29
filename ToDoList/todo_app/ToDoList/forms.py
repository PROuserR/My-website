from django import forms
from .models import Task


#To edit a task
class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'note', 'high_priority','finished']


#To make a new task
class NewTaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'note', 'high_priority', 'daily']