from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from .models import *

def post_list(request):
    posts = Post.objects.all().order_by('-created_at')

    for post in posts:
        post.is_liked = post.likes.filter(user=request.user).exists()
        
    return render(request, 'post_template.html', {'posts': posts})

def toggle_like(request, post_id):
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'Not authenticated'}, status=401)

    post = Post.objects.get(id=post_id)
    like, created = Like.objects.get_or_create(user=request.user, post=post)

    if not created:
        like.delete()
        liked = False
    else:
        liked = True

    likes_count = post.likes.count()
    return JsonResponse({'liked': liked, 'likes_count': likes_count})

def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    return render(request, 'post_detail.html', {'post': post})

def add_comment(request, post_id):
    if request.method == "POST":
        post = get_object_or_404(Post, id=post_id)
        text = request.POST.get("text")

        if request.user.is_authenticated and text:
            Comment.objects.create(
                post=post,
                user=request.user,
                text=text
            )

        return redirect('post_detail', post_id=post.id)

def create_post(request):
    if request.method == "POST":
        text = request.POST.get("text")
        if text:
            Post.objects.create(text=text, user=request.user)
            return redirect('post_list')
    return render(request, 'create_post.html')