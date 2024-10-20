from django.shortcuts import render, get_object_or_404
from .models import Post, Comment
from django.views.decorators.cache import cache_page
from django.contrib.auth.decorators import login_required
from django.core.cache import cache
from django.http import HttpResponseRedirect
from django.urls import reverse

def blog_list(request):
    posts = Post.objects.all().prefetch_related('comments__author', 'tags')
    print(posts.query)
    return render(request, 'index.html', {'posts':posts})

@cache_page(60)
def post_list(request):
    posts = Post.objects.all().prefetch_related('comments__author', 'tags')
    print(posts.query)
    return render(request, 'index.html', {'posts':posts})


def blog_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    recent_comments = Comment.objects.filter(post=post).select_related('author').order_by('-created_date')
    context = {
        'post': post,
        'recent_comments': recent_comments,
    } 
    return render(request, "post_detail.html", context)

def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    recent_comments_cache_key = f'recent_comments_post_{post.id}'
    
    recent_comments = cache.get(recent_comments_cache_key)
    if not recent_comments:
        recent_comments = Comment.objects.filter(post=post).select_related('author').order_by('-created_date')
        cache.set(recent_comments_cache_key, recent_comments, timeout=60)
    
    comment_count_cache_key = f'comment_count_post_{post.id}'
    comment_count = cache.get(comment_count_cache_key)
    if comment_count is None:
        comment_count = Comment.objects.filter(post=post).count()
        cache.set(comment_count_cache_key, comment_count, timeout=300)
    
    context = {
        'post': post,
        'recent_comments': recent_comments,
        'recent_comments_cache_key': recent_comments_cache_key,
        'comment_count': comment_count,
    }
    return render(request, 'post_detail.html', context)

@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    content = request.POST.get('content')
    author = request.user
    
    if content:
        Comment.objects.create(post=post, author=author, content=content)
        
        comment_count_cache_key = f'comment_count_post_{post.id}'
        cache.delete(comment_count_cache_key)
        
        recent_comments_cache_key = f'recent_comments_post_{post.id}'
        cache.delete(recent_comments_cache_key)
    
    return HttpResponseRedirect(reverse('post_detail', args=[post.id]))