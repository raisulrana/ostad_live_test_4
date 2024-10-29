from django.shortcuts import render, redirect
from .import forms
from .import models
from .models import Post
from categories.models import Category
from django.db.models import Q

def homepage(request):
    query = request.GET.get('q')  # Get the search query from the request
    if query:
        # Filter posts by title or category name
        posts = Post.objects.filter(
            Q(title__icontains=query) | 
            Q(category__name__icontains=query)
        ).distinct()  # distinct() to remove duplicate results if any
    else:
        # If no query, return all posts
        posts = Post.objects.all()
    
    return render(request, 'home.html', {'data': posts})

def add_post(request):
    if request.method == 'POST':
        post_form = forms.PostForm(request.POST)
        if post_form.is_valid():
            post_form.save()
            return redirect('add_post')
        
    else:
        post_form = forms.PostForm()
        
    return render(request, 'add_post.html',{'form': post_form})


def edit_post(request, id):
    post = models.Post.objects.get(pk=id)
    post_form = forms.PostForm(instance=post)
    if request.method == 'POST':
        post_form = forms.PostForm(request.POST)
        if post_form.is_valid():
            post_form.save()
            return redirect('add_post')
        
    else:
        post_form = forms.PostForm()
        
    return render(request, 'add_post.html',{'form': post_form})

def delete_post(request, id):
    post = models.Post.objects.get(pk=id)
    post.delete()
    
    return redirect ('homepage')