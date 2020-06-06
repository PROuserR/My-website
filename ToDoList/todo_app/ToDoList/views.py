from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import Http404
from .models import Task
from .forms import TaskForm, NewTaskForm
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


# Create your views here.
def index(request):
    if request.user.is_authenticated:
        if request.method != 'POST':
            weekly_tasks = Task.objects.filter(owner=request.user, weekly=True).order_by('-high_priority')
            if len(weekly_tasks) > 0:
                now = datetime.datetime(
                    time.localtime().tm_year, time.localtime().tm_mon, time.localtime().tm_mday)
                

                finished_weekly_tasks = list(
                    filter(lambda task: task.finished == True, weekly_tasks))
                weekly_average = f'{100 * len(finished_weekly_tasks)// len(weekly_tasks)}%'
            else:
                weekly_tasks = None
                weekly_average = None
            #Vars for fullcalendar.js

            weekly_tasks_date_added = []
            for weekly_task in weekly_tasks:
                #add zeros before month and day so fullcalendar can render them
                year = str(weekly_task.date_added.year)
                month = str(weekly_task.date_added.month)
                day = str(weekly_task.date_added.day)
                hour = str(weekly_task.date_added.hour)
                minute = str(weekly_task.date_added.minute)
                second = str(weekly_task.date_added.second)
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
                weekly_tasks_date_added.append(date_added)

            context = {'weekly_tasks': [weekly_task.title for weekly_task in weekly_tasks],
                       'weekly_tasks_date_added': weekly_tasks_date_added,
                       'weekly_tasks_id': [weekly_task.id for weekly_task in weekly_tasks],
                       'weekly_tasks_high_priority': [weekly_task.high_priority for weekly_task in weekly_tasks],
                       'weekly_average': weekly_average,
                       'link': link,
                       'tips': choice(tips)}
            return render(request, "index.html", context)
        else:
            weekly_task = Task.objects.get(id=request.POST.get('id'))
            weekly_task.finished = True
            weekly_task.save()
            return redirect('ToDoList:index')
    else:
        return render(request, "index.html")


def accounts_profile(request):
    return redirect('ToDoList:index')


@login_required
def unfinished_tasks(request):
    unfinished_tasks = Task.objects.filter(owner=request.user, finished=False, weekly=False).order_by('-high_priority')
    if request.method == 'POST':
        task = Task.objects.get(id=request.POST.get("id"))
        task.delete()
        return redirect("ToDoList:unfinished_tasks")

    context = {"unfinished_tasks": unfinished_tasks, 
                'tips': choice(tips)}
    return render(request, "unfinished_tasks.html", context)


@login_required
def finished_tasks(request):
    finished_tasks = Task.objects.filter(owner=request.user, finished=True, weekly=False).order_by('-high_priority')
    context = {"finished_tasks": finished_tasks, 
                'tips': choice(tips)}
    return render(request, "finished_tasks.html", context)


@login_required
def edit_task(request, task_id):
    task = Task.objects.get(id=task_id)

    if request.method == "GET":
        form = TaskForm(instance=task)
    elif request.method == "POST":
        form = TaskForm(instance=task, data=request.POST)
        if request.POST.get("submit") == "Remove":
            task.delete()
        else:
            if form.is_valid():
                task.title = form["title"].value()
                task.finished = form["finished"].value()
                task.note = form["note"].value()
                task.high_priority = form["high_priority"].value()
                task.save()

        return redirect("ToDoList:index")
    if task.owner != request.user:
        raise Http404

    context = {"form": form, 'task': task}
    return render(request, "edit_task.html", context)


@login_required
def new_task(request):
    if request.method != "POST":
        form = NewTaskForm()
    else:
        form = NewTaskForm(data=request.POST)
        if form.is_valid():
            new_task = form.save(commit=False)
            new_task.owner = request.user
            new_task.save()
            return redirect("ToDoList:index")

    context = {"form": form}
    return render(request, "new_task.html", context)


@login_required
def search_results(request):
    search_query = request.POST.get("search")
    tasks = []
    for task in Task.objects.filter(owner=request.user):

        if search_query.upper() in task.title.upper():
            tasks.append(task)

    context = {"tasks": tasks}
    return render(request, "search_results.html", context)