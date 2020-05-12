from django.test import TestCase
from .models import Task

# Create your tests here.
class TaskTest(TestCase):

    def test_daily_finished(self):
        tasks = Task.objects.filter(daily=True)

        for task in tasks:
            if task.finished:
                self.assertIs(task.finished, True)
            else:
                self.assertIs(task.finished, True)
