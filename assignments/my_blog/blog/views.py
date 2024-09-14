from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Post, Comment
from .forms import PostForm, CommentForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

def print_hello(request):
    return HttpResponse("Hello, Blog!")

def list_blogs(request):
    posts = Post.objects.all()
    paginator = Paginator(posts, 3)

    page = request.GET.get('page')
    page_posts = paginator.get_page(page)
    return render(request, "index.html", {"posts": page_posts})

def get_blog(request, id):
    post = Post.objects.get(id=id)
    commentForm = CommentForm()

    context = {
        'post': post,
        'CommentForm': commentForm
    }
    return render(request, "blog_detail.html", context)

@login_required
def add_blog(request):
    if(request.method == 'POST'):
        form = PostForm(request.POST)
        if form.is_valid():
            blog = form.save(commit=False)
            blog.author = request.user
            blog.save()
            return HttpResponse("Ok")
        else:
            raise Exception(f"Error: {form.errors}")
    else:
        form = PostForm()
    return render(request, 'add_blogs.html', {'form': form})

@login_required
def delete_blog(request, id):
    post_obj = Post.objects.get(id=id)

    if(post_obj.author != request.user):
        return redirect('home')
    
    post_obj.delete()
    return redirect('home')

@login_required
def edit_blog(request, id):
    post = get_object_or_404(Post, id=id)

    if(post.author != request.user):
        return redirect('home')
    if(request.method == 'POST'):
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect("blog_detail", id=post.id)
    else:
        form = PostForm(instance=post)

    return render(request, 'edit_blog.html', {'form': form})

@login_required
def add_comment(request, id):
    post = get_object_or_404(Post, id=id)
    if(request.method == 'POST'):
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.post = post
            comment.save()
            return redirect("blog_detail",id=post.id)
        else:
            raise Exception(f"Error: {form.errors}")
    return render(request, 'blog_detail.html')

def login_view(request):
    if (request.method == 'POST'):
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            try:
                user = authenticate(**form.cleaned_data)
                login(request, user)
                return redirect("home")
            except Exception:
                return HttpResponse("something is not ok")
        else:
            raise Exception(f"some erros {form.errors}")
    return render(request, 'login.html', {'form': AuthenticationForm()})

def register_view(request):
    if(request.method == 'POST'):
        form = UserCreationForm(data=request.POST)
        if(form.is_valid()):
            form.save()
            return redirect("login")
        else:
            raise Exception(f"some erros {form.errors}")
    return render(request, 'register.html', {'form':UserCreationForm()})

def logout_view(request):
    logout(request)
    return redirect("home")