from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from random import choice
from .models import Project, TreeField
from .forms import ProjectForm
from ToDoList.models import Task


link = 'https://www.verywellmind.com/things-you-can-do-to-improve-your-mental-focus-4115389'
tips = ['Start by Assessing Your Mental Focus',
        'Eliminate Distractions',
        'Focus on One Thing at a Time',
        'Live in the Moment',
        'Practice Mindfulness',
        'Try Taking a Short Break',
        'Keep Practicing to Strengthen Your Focus']


# Create your views here.
@login_required
def projects(request):
    projects = Project.objects.filter(admin=request.user, finished=False)
    tasks = []
    members = []
    for project in projects:
        task_ids = project.tasks.split(',')
        member_ids = project.members.split(',')

        for task_id in task_ids:
            if task_id.isnumeric():
                tasks.append(Task.objects.get(id=int(task_id)))

        for member_id in member_ids:
            if member_id.isnumeric():
                members.append(User.objects.get(id=int(member_id)))

    context = {'projects': projects,
    'tasks': tasks,
    'members': members,
    'tip': choice(tips),
    'link': link}
    return render(request, 'projects.html', context)
    


@login_required
def project(request, project_id):
    project = Project.objects.get(id=project_id)
    project_data = None
    if project.type == 'tree':
        trees = TreeField.objects.all()
        for tree in trees:
            if tree.project == project:
                project_data = tree
    if project.type == 'linear':
        tasks_id = project.tasks
        tasks = Task.objects.filter(project=True)
        #Tasks with the required id
        tasks = list(filter(lambda task: str(task.id) in tasks_id, tasks))
        project_data = tasks

        print(project.tasks, project.members)

    context = {'project_data':project_data}
    return render(request, 'project.html', context)

@login_required
def new_project(request):
    if request.method != 'POST':
        form = ProjectForm()
    else:
        form = ProjectForm(data=request.POST)
        if form.is_valid():
            new_project = form.save(commit=False)
            new_project.admin = request.user
            new_project.save()
            return redirect('Projects:projects')
    
    context = {'form':form}
    return render(request, 'new_project.html', context)


def edit_project(request, project_id):
    project = Project.objects.get(id=project_id)
    tasks = Task.objects.filter(owner=request.user, project=True)
    members = User.objects.exclude(username=request.user.username)

    if request.method != 'POST':
        form = ProjectForm(instance=project)
    else:
        form = ProjectForm(instance=project, data=request.POST)
        if request.POST.get('submit') == 'delete':
            project.delete()
        else:
            if form.is_valid():
                form.save()
                if f"{request.POST.get('tasks')}," not in project.tasks:
                    project.tasks += f"{request.POST.get('tasks')},"
                if f"{request.POST.get('members')}," not in project.members:
                    project.members += f"{request.POST.get('members')},"
                project.save()

        return redirect('Projects:projects')

    context = {'form': form, 'project': project, 'tasks': tasks, 'members':members}
    return render(request, 'edit_project.html', context)