from django.urls import path, include
from . import views

app_name = "Users"
urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    path('edit_profile/<int:user_id>', views.edit_profile, name='edit_profile')
]