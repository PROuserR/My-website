from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import Http404
from .models import WeeklyTask, Task
from .forms import TaskForm, NewTaskForm, NewWeeklyTaskForm, WeeklyTaskForm
from random import choice
import datetime
import time


link = 'https://www.verywellmind.com/things-you-can-do-to-improve-your-mental-focus-4115389'
tips = ['Start by Assessing Your Mental Focus',
        'Eliminate Distractions',
        'Focus on One Thing at a Time',
        'Live in the Moment',
        'Practice Mindfulness',
        'Try Taking a Short Break',
        'Keep Practicing to Strengthen Your Focus']


# Create your views here.
def index(request):
    if request.user.is_authenticated:
        weekly_tasks = WeeklyTask.objects.filter(owner = request.user).order_by('-high_priority')
        print(weekly_tasks)
        for weekly_task in weekly_tasks:
            if weekly_task.date_tobe_finished.year >= datetime.datetime.now().year:
                if weekly_task.date_tobe_finished.month >= datetime.datetime.now().month:
                    if weekly_task.date_tobe_finished.day >= datetime.datetime.now().day:
                        weekly_task.finished = False
                        weekly_task.save()
        context = { 'weekly_tasks': weekly_tasks,
        'days': set([weekly_task.day for weekly_task in weekly_tasks]),
        'tip': choice(tips),
        'link': link}

        return render(request, 'index.html', context)
    else:
        return render(request, 'index.html')


@login_required
def new_weekly_task(request):
    if request.method != 'POST':
        form = NewWeeklyTaskForm()
    else:
        form = NewTaskForm(data=request.POST)
        if form.is_valid():
            new_weekly_task = form.save(commit=False)
            new_weekly_task.owner = request.user
            new_weekly_task.day = new_weekly_task.day.lower()
            day = datetime.datetime.now().day + 7
            month = datetime.datetime.now().month
            year = datetime.datetime.now().year
            if day + 7 > 30:
                day = abs(day - 30)
                month += 1
            if month > 12:
                month = 1
                year += 1
            new_weekly_task.date_tobe_finished = datetime.date(year, month, day)
            new_weekly_task.save()
            return redirect('ToDoList:index')
    
    context = {'form': form}
    return render(request, 'new_weekly_task.html', context)


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
            return redirect('ToDoList:tasks')

    context = {'form': form}
    return render(request, 'new_task.html', context)


@login_required
def tasks(request):
    tasks = Task.objects.filter(owner=request.user, finished=False, project=False).order_by('-high_priority')
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
               'tip': choice(tips),
               'link': link}
    return render(request, 'tasks.html', context)


@login_required
def edit_task(request, task_id):
    task = Task.objects.get(id=task_id)

    if request.method != 'POST':
        form = TaskForm(instance=task)
    else:
        form = TaskForm(instance=task, data=request.POST)
        if request.POST.get('submit') == 'delete':
            task.delete()
            return redirect('ToDoList:tasks')
        else:
            if form.is_valid():
                form.save()
                return redirect('ToDoList:tasks')

    context = {'form': form, 'task': task}
    return render(request, 'edit_task.html', context)


@login_required
def edit_weekly_task(request, weekly_task_id):
    weekly_task = WeeklyTask.objects.get(id=weekly_task_id)

    if request.method != 'POST':
        form = WeeklyTaskForm(instance=weekly_task)
    else:
        form = WeeklyTaskForm(instance=weekly_task, data=request.POST)
        if request.POST.get('submit') == 'delete':
            weekly_task.delete()
            return redirect('ToDoList:index')
        else :
            if form.is_valid():
                form.save()
                return redirect('ToDoList:index')

    context = {'form': form, 'weekly_task': weekly_task}
    return render(request, 'edit_weekly_task.html', context)

@login_required
def finish_weekly_task(request, weekly_task_id):
    weekly_task = WeeklyTask.objects.get(id=weekly_task_id)
    weekly_task.finished = True
    weekly_task.save()
    return redirect('ToDoList:index')


@login_required
def search_results(request):
    search_query = request.POST.get('search')
    tasks = []
    for task in Task.objects.filter(owner=request.user):

        if search_query.upper() in task.title.upper():
            tasks.append(task)

    context = {'tasks': tasks}
    return render(request, 'search_results.html', context)


def accounts_profile(request):
    return redirect('ToDoList:index')