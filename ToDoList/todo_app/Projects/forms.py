from django import forms
from .models import Project
from tempus_dominus.widgets import DatePicker, TimePicker, DateTimePicker


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['name', 'description', 'type', 'rules', 'finished', 'date_to_be_finished']
        widgets = {'date_to_be_finished': DateTimePicker(
            options={
                'useCurrent': True,
                'collapse': False,
            },
            attrs={
                'append': 'fa fa-clock',
                'icon_toggle': True,
            })}