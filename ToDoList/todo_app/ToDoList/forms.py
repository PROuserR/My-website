from django import forms
from .models import Task, WeeklyTask
from tempus_dominus.widgets import DatePicker, TimePicker, DateTimePicker


#To edit a task
class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'note', 'high_priority','finished', 'project']


#To make a new task
class NewTaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'note', 'high_priority', 'project']


class WeeklyTaskForm(forms.ModelForm):
    class Meta:
        model = WeeklyTask
        fields = ['title', 'note', 'high_priority', 'day', 'hour', 'finished']
        widgets = {'hour': TimePicker(
            options={
                'format': 'hh:mm'
            },
            attrs={
                'append': 'fa fa-clock',
                'icon_toggle': True,
            },
        )}


class NewWeeklyTaskForm(forms.ModelForm):
    class Meta:
        model = WeeklyTask
        fields = ['title', 'note', 'high_priority', 'day', 'hour']
        widgets = {'hour': TimePicker(
            options={
                'format': 'hh:mm'
            },
            attrs={
                'append': 'fa fa-clock',
                'icon_toggle': True,
            },
        )}