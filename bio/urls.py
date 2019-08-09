from django.urls import path, include
from . import views

app_name = 'bio'

urlpatterns = [
    path('overview/', views.overview, name='overview'),
    path('personality', views.personality, name='personality'),
    path('movies/', views.movies, name='movies'),
    path('trailers/', views.trailers, name='trailers'),
    path('faq/', views.faq, name='faq'),
    path('edit_answer/<int:id>', views.edit_answer, name='edit_answer'),
    path('add_answer/<int:id>', views.add_answer, name='add_answer'),
    path('add_question/', views.add_question, name='add_question'),
]