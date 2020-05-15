from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import Http404
from .models import Task
from .forms import TaskForm, NewTaskForm
from random import choice
import datetime
import time

# Create your views here.
def index(request):
    if request.user.is_authenticated:
        link = 'https://www.verywellmind.com/things-you-can-do-to-improve-your-mental-focus-4115389'
        tips = ['Start by Assessing Your Mental Focus',
                'Eliminate Distractions',
                'Focus on One Thing at a Time',
                'Live in the Moment',
                'Practice Mindfulness',
                'Try Taking a Short Break',
                'Keep Practicing to Strengthen Your Focus']

        if request.method != 'POST':
            daily_tasks = Task.objects.filter(owner=request.user, daily=True).order_by('-high_priority')

            if len(daily_tasks) > 0:
                now = datetime.datetime(
                    time.localtime().tm_year, time.localtime().tm_mon, time.localtime().tm_mday)
                

                for daily_task in daily_tasks:
                    if daily_task.date_added.day != now.day:
                        daily_task.date_added = now
                        daily_task.finished = False
                        daily_task.save()

                finished_daily_tasks = list(
                    filter(lambda task: task.finished == True, daily_tasks))
                daily_average = f'{100 * len(finished_daily_tasks)/ len(daily_tasks)}%'
            else:
                daily_tasks = None
                daily_average = None

            context = {'daily_tasks': daily_tasks,
                       'daily_average': daily_average,
                       'link': link,
                       'tips': choice(tips)}
            return render(request, "index.html", context)
        else:
            daily_task = Task.objects.get(id=request.POST.get('id'))
            daily_task.finished = True
            daily_task.save()
            return redirect('ToDoList:index')
    else:
        return render(request, "index.html")


@login_required
def unfinished_tasks(request):
    unfinished_tasks = Task.objects.filter(owner=request.user, finished=False, daily=False).order_by('-high_priority')
    if request.method == 'POST':
        task = Task.objects.get(id=request.POST.get("id"))
        task.delete()
        return redirect("ToDoList:unfinished_tasks")

    context = {"unfinished_tasks": unfinished_tasks}
    return render(request, "unfinished_tasks.html", context)


@login_required
def finished_tasks(request):
    finished_tasks = Task.objects.filter(owner=request.user, finished=True, daily=False).order_by('-high_priority')
    context = {"finished_tasks": finished_tasks}
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
        if search_query in task.title:
            tasks.append(task)

    context = {"tasks": tasks}
    return render(request, "search_results.html", context)