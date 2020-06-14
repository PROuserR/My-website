from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from ToDoList.models import Task, WeeklyTask
from Projects.models import Project
import datetime
import time


# Create your views here.
def register(request):
    if request.method != 'POST':
        form = UserCreationForm()
    else:
        form = UserCreationForm(data=request.POST)
        if form.is_valid():
            new_user = form.save()
            login(request, new_user)
            return redirect('ToDoList:index')

    context = {'form': form}
    return render(request, 'registration/register.html', context)


@login_required
def profile(request):
    now = datetime.datetime(
        time.localtime().tm_year, time.localtime().tm_mon, time.localtime().tm_mday)

    projects = Project.objects.filter(
        admin=request.user, finished=True)
    projects_len = len(projects)


    weekly_tasks = WeeklyTask.objects.filter(
        owner=request.user, finished=True)
    weekly_tasks_len = len(weekly_tasks)

    tasks = Task.objects.filter(
        owner=request.user, finished=True)
    tasks_len = len(tasks)
    if tasks_len > 0:
        # Fetching required data from imported models for doing some data visualization
        date_joined = request.user.date_joined
        dates = []
        for task in tasks:
            dates.append(datetime.datetime(task.date_added.year,
                                           task.date_added.month, task.date_added.day))
        tasks_per_day = {}
        for date in dates:
            tasks_per_day[date] = dates.count(date)
        progress = {}
        for i in range(now.day - date_joined.day + 1):
            date = datetime.datetime(
                now.year, now.month, i + date_joined.day).timetuple()
            date = f'{date.tm_year}/{date.tm_mon}/{date.tm_mday}'
            if datetime.datetime(now.year, now.month, i + date_joined.day) in dates:
                progress[date] = tasks_per_day[datetime.datetime(
                    now.year, now.month, i + date_joined.day)]
            else:
                progress[date] = 0
        
        task_sum = 0
        for task in progress.values():
            task_sum += task
        try:
            if task_sum/len(progress.keys()) >= 1:
                well_done = True
            else:
                well_done = False
        except ZeroDivisionError:
            well_done = False

        average = f'{task_sum} task(s) per {len(progress.keys())} day(s)'

        last_task = tasks.last()

        context = {'tasks_len': tasks_len, 'weekly_tasks_len': weekly_tasks_len, 
                   'projects_len': projects_len,
                   'average': average, 'well_done': well_done, 'last_task': last_task,
                   'x_values': list(progress.keys()), 'y_values': list(progress.values())}
        return render(request, 'profile.html', context)
    else:
        context = {'tasks_len': tasks_len}
        return render(request, 'profile.html', context)
