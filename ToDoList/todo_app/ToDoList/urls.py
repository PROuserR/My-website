from django.urls import path
from . import views

app_name = 'ToDoList'
urlpatterns = [
    path('', views.index, name='index'),
    path('tasks/', views.tasks, name='tasks'),
    path('new_task/', views.new_task, name='new_task'),
    path('new_weekly_task', views.new_weekly_task, name='new_weekly_task'),
    path('edit_task/<int:task_id>', views.edit_task, name='edit_task'),
    path('search_results/', views.search_results, name='search_results'),
    path('accounts/profile/', views.accounts_profile, name='accounts_profile'),
]