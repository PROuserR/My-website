from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import Http404
from .models import Task, WeeklyTask
from .forms import TaskForm, NewTaskForm, NewWeeklyTaskForm
from random import choice
import datetime
import time

#These vars are global to be used by funcs that view your tasks
link = 'https://www.verywellmind.com/things-you-can-do-to-improve-your-mental-focus-4115389'
tips = ['Start by Assessing Your Mental Focus',
        'Eliminate Distractions',
        'Focus on One Thing at a Time',
        'Live in the Moment',
        'Practice Mindfulness',
        'Try Taking a Short Break',
        'Keep Practicing to Strengthen Your Focus']


def check_day(day):
    if day.lower() in ['sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday']:
        return True

    return False


def check_time(time):
    try:
        hour = time[:2]
        minute = time[3:5]
        part = time[5:7]
    except ValueError:
        print(ValueError())
    finally:
        hour = time[0]
        minute = time[2:4]
        part = time[4:6]

    if int(hour) > 0 and int(hour) < 13:
        if int(minute) >= 0 and int(minute) < 60:
            if part.lower() == 'am' or part.lower() == 'pm':
                return True
    
    return False


# Create your views here.
def index(request):
    if request.user.is_authenticated:
        weekly_tasks = WeeklyTask.objects.filter(owner = request.user).order_by('-high_priority')
        context = {'tip': choice(tips), 'weekly_tasks': weekly_tasks}
        return render(request, 'index.html', context)
    else:
        return render(request, 'index.html')


def accounts_profile(request):
    return redirect('ToDoList:index')


@login_required
def new_weekly_task(request):
    if request.method != 'POST':
        form = NewWeeklyTaskForm()
    else:
        form = NewWeeklyTaskForm(data=request.POST)
        if form.is_valid():
            if check_day(form['day'].value()):
                if check_time(form['hour'].value()):
                    new_weekly_task = form.save(commit=False)
                    new_weekly_task.owner = request.user
                    new_weekly_task.day = new_weekly_task.day.lower()
                    new_weekly_task.save()
                    return redirect('ToDoList:index')
    
    context = {'form': form}
    return render(request, 'new_weekly_task.html', context)


@login_required
def tasks(request):
    tasks = Task.objects.filter(owner=request.user, finished=False).order_by('-high_priority')
    if request.method == 'POST':
        task = Task.objects.get(id=request.POST.get('id'))
        task.delete()
        return redirect('ToDoList:tasks')
    else:
        tasks_date_added = []
        for task in tasks:
            #add zeros before month and day so fullcalendar can render them
            year = str(task.date_added.year)
            month = str(task.date_added.month)
            day = str(task.date_added.day)
            hour = str(task.date_added.hour)
            minute = str(task.date_added.minute)
            second = str(task.date_added.second)
            #We need to put zeroes before the number so fullcalendar can accpect it
            if int(month) < 10:
                month = f'0{month}'
            if int(day) < 10:
                day = f'0{day}'
            if int(hour) < 10:
                hour = f'0{hour}'
            if int(minute) < 10:
                minute = f'0{minute}'
            if int(second) < 10:
                second = f'0{second}'
            date_added = f'{year}-{month}-{day}T{hour}:{minute}:{second}'
            tasks_date_added.append(date_added)
    context = {'tasks': [task.title for task in tasks], 
               'tasks_date_added': tasks_date_added,
               'tasks_id': [task.id for task in tasks],
               'tasks_high_priority': [task.high_priority for task in tasks],
               'tip': choice(tips)}
    return render(request, 'tasks.html', context)


@login_required
def edit_task(request, task_id):
    task = Task.objects.get(id=task_id)

    if request.method == 'GET':
        form = TaskForm(instance=task)
    elif request.method == 'POST':
        form = TaskForm(instance=task, data=request.POST)
        if request.POST.get('submit') == 'Remove':
            task.delete()
        else:
            if form.is_valid():
                task.title = form['title'].value()
                task.finished = form['finished'].value()
                task.note = form['note'].value()
                task.high_priority = form['high_priority'].value()
                task.save()

        return redirect('ToDoList:index')
    if task.owner != request.user:
        raise Http404

    context = {'form': form, 'task': task}
    return render(request, 'edit_task.html', context)


@login_required
def new_task(request):
    if request.method != 'POST':
        form = NewTaskForm()
    else:
        form = NewTaskForm(data=request.POST)
        if form.is_valid():
            new_task = form.save(commit=False)
            new_task.owner = request.user
            new_task.save()
            return redirect('ToDoList:index')

    context = {'form': form}
    return render(request, 'new_task.html', context)


@login_required
def search_results(request):
    search_query = request.POST.get('search')
    tasks = []
    for task in Task.objects.filter(owner=request.user):

        if search_query.upper() in task.title.upper():
            tasks.append(task)

    context = {'tasks': tasks}
    return render(request, 'search_results.html', context)