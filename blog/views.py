from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from datetime import datetime
from .models import Post
from .forms import PostCreateForm, UserLoginForm
from django.contrib.auth import authenticate, login

def post_list(request):
    posts = Post.objects.all()
    context = {
        'posts':posts
    }
    return render(request, 'blog/post_list.html', context)

def post_detail(request, p_id, p_slug):
    post = get_object_or_404(Post, pk=p_id, slug=p_slug)
    context = {
        'post':post
    }
    return render(request, 'blog/post_detail.html', context)

def post_create(request):
    if request.method == 'POST':
        form = PostCreateForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
    else:
        form = PostCreateForm()

    context = {
        'form': form
    }
    return render(request, 'blog/post_create.html', context)

def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)
            if user :
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect(reverse('post_list'))
                else:
                    return HttpResponse('user is not active')
            else:
                return HttpResponse('user is none')
    else:
        form = UserLoginForm()

    context = {
        'form':form ,
    }
    return render(request, 'blog/login.html', context)
