from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('blogs/', views.blogs, name='blogs'),
    path('blog/<int:blog_id>/', views.blog, name='blog'),
    path('new_blog/', views.new_blog, name='new_blog'),
    path('new_entry/<int:blog_id>/', views.new_entry, name='new_entry'),
]