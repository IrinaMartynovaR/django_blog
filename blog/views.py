from django.shortcuts import render, get_object_or_404
from django.http import Http404
from django.utils import timezone
from django.contrib.auth.decorators import login_required

from .forms import PostForm
from .models import Post

@login_required
def post_edit(request, id):
    post = get_object_or_404(Post, id=id) if id else None

    if post and post.author !=request.user:
        return redirect('post_list')

    if request.method == "Post":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post=form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', id=post.id)
        else:
            form = PostForm(instance=post)
        return render(request, 'blog/post_edit.html', {'form': form})



def post_update(request, id):
    post = get_object_or_404 (Post, id=id) if id else None

    if post and post.author != request.user:
        return redirect('post_list')

    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', id=post.id)
        else:
            form = PostForm(instance=post)
        return render(request, 'blog/post_edit.html', {'form': form})
    return redirect('post_list')

def post_add(request):
    if request.method == "Post":
        form = PostForm(request.Post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', id=post.id)
        else:
            form = PostForm(instance=post)
        return render(request, 'blog/post_edit.html', {'form': form})

def post_list(request):
    posts = Post.objects.for_user(user=request.user)
    return render(request, 'blog/post_list.html', {'posts': posts})

def post_detail(request, id):
    post = Post.objects.get(id=id)
    return render(request, 'blog/post_detail.html', {'post': post})

def handler404(request, exception, template_name = "404"):
    response = render("404.html")
    response.status_code = 404
    return response