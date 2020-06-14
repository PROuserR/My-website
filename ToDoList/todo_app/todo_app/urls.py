from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('ToDoList.urls')),
    path('users/', include('Users.urls')),
    path('', include('Projects.urls')),
    path('accounts/', include('allauth.urls')),
]
