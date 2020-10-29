from django.urls import path
from . import views

app_name = 'Projects'
urlpatterns = [
    path('projects/', views.projects, name='projects'),
    path('project/<int:project_id>', views.project , name='project'),
    path('edit_project/<int:project_id>', views.edit_project, name='edit_project'),
    path('new_project/', views.new_project, name='new_project'),
]