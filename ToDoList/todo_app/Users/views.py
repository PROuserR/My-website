from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from ToDoList.models import Task, Task
from Projects.models import Project
from .models import Profile
from .forms import EditProfileForm, EditUserForm
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
    now = datetime.datetime(time.localtime().tm_year, time.localtime().tm_mon, time.localtime().tm_mday)

    projects = Project.objects.filter(admin=request.user, finished=True)
    projects_len = len(projects)

    weekly_tasks = Task.objects.filter(owner=request.user, finished=True)
    weekly_tasks_len = len(weekly_tasks)

    tasks = Task.objects.filter(owner=request.user, finished=True)
    tasks_len = len(tasks)

    try:
        profile = Profile.objects.get(owner=request.user)
        profile_pic = profile.profile_pic
    except Exception as e:
        profile_pic = None
        print(e)

    
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
                   'x_values': list(progress.keys()), 'y_values': list(progress.values())
                   ,'profile_pic': profile_pic, 'now': now.isoformat()}

        return render(request, 'profile.html', context)
    else:
        context = {'tasks_len': tasks_len, 'projects_len': 0, 'weekly_tasks_len': 0,
                   'average': 0, 'last_task': None,
                   'profile_pic': profile_pic}
        return render(request, 'profile.html', context)


def edit_profile(request, user_id):
    if request.method != 'POST':
        profile_form = EditProfileForm()
        user_form = EditUserForm()
    else:
        profile_form = EditProfileForm(request.POST, request.FILES)
        user_form = EditUserForm(request.POST)
        if request.POST.get('submit') == 'delete':
            request.user.delete()
            return redirect('ToDoList:index')
        else:
            if profile_form.is_valid() or user_form.is_valid():
                profiles = Profile.objects.all()
                if len(profiles) == 0:
                    profile = profile_form.save(commit=False)
                    profile.profile_pic = request.FILES['profile_pic']
                    profile.owner = request.user
                    profile.save()
                else:
                    for profile in profiles:
                        #Ensuring the image is existed
                        try:
                            if str(request.user) in str(profile.owner):
                                profile = Profile.objects.get(owner=request.user)
                                profile.profile_pic = request.FILES['profile_pic']
                                profile.save()
                            else:
                                profile = profile_form.save(commit=False)
                                profile.profile_pic = request.FILES['profile_pic']
                                profile.owner = request.user
                                profile.save()
                        except Exception as e:
                            print(e)

                    user = User.objects.get(id=request.user.id)
                    if request.POST['username']:
                        user.username = request.POST['username']
                    if request.POST['password']:
                        user.password = request.POST['password']
                    if request.POST['email']:
                        user.email = request.POST['email']
                    user.save()
                
            return redirect('Users:profile')

    context = {'profile_form': profile_form, 'user_form': user_form}
    return render(request, 'edit_profile.html', context)