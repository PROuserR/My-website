from django.urls import path
from . import views

app_name = 'ToDoList'
urlpatterns = [
    path('', views.index, name='index'),
    path('unfinished_tasks/', views.unfinished_tasks, name='unfinished_tasks'),
    path('finished_tasks/', views.finished_tasks, name='finished_tasks'),
    path('new_task/', views.new_task, name='new_task'),
    path('edit_task/<int:task_id>', views.edit_task, name='edit_task'),
    path('search_results/', views.search_results, name='search_results'),
]