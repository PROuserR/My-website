from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Blog, Entry
from .forms import BlogForm, EntryForm, CommentForm
import os

# Create your views here.
@login_required
def blogs(request):
    print(request)
    blogs = Blog.objects.order_by('date_added')
    context = {'blogs': blogs}
    return render(request, 'blogs.html', context)


@login_required
def blog(request, blog_id):
    blog = Blog.objects.get(id=blog_id)
    entries = blog.entry_set.order_by('-date_added')
    for entry in entries:
        print(entry.comment_set.order_by('-date_added'))

    if request.method != 'POST':
        form = CommentForm()
    else:
        form = CommentForm(data=request.POST)

        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.entry = Entry.objects.get(id=request.POST['entry_id'])
            new_comment.save()
            return redirect('blog:blog', blog_id)

    context = {'blog': blog, 'entries': entries, 'form': form}
    return render(request, 'blog.html', context)


@login_required
def new_blog(request):
    if request.method != 'POST':
        form = BlogForm()
    else:
        form = BlogForm(data=request.POST)

        if form.is_valid():
            new_blog = form.save(commit=False)
            new_blog.owner = request.user
            new_blog.save()
            return redirect('blog:blogs')
    
    context = {'form': form}
    return render(request, 'new_blog.html', context)


@login_required
def new_entry(request, blog_id):
    blog = Blog.objects.get(id=blog_id)

    if request.method != 'POST':
        form = EntryForm()
    else:
        if request.method == 'POST':
            form = EntryForm(request.POST, request.FILES)

            if form.is_valid():
                new_entry = form.save(commit=False)
                new_entry.blog = blog  
                new_entry.save()
                try:
                    os.replace(new_entry.image.name, f'{os.getcwd()}/blog/static/{new_entry.image.name}')
                except:
                    print('An error happend check file availablity')

                return redirect('blog:blog', blog_id=blog_id)

    context = {'form': form, 'blog': blog}
    return render(request, 'new_entry.html', context)