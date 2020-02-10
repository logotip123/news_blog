from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.shortcuts import render, get_object_or_404

from .forms import PostForm, CommentForm
from .models import Post, Comment


def get_index(request):
    posts = Post.objects.filter(status=1).all()
    return render(request, 'blog/index.html', {'posts': posts})


@login_required
def add_post(request):
    form = PostForm()
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            if request.user.groups.filter(name='Users').first() is not None:
                status = 0
            else:
                status = 1
            try:
                Post(
                    title=form.cleaned_data['title'],
                    content=form.cleaned_data['content'],
                    author=request.user,
                    status=status
                ).save()
            except IntegrityError:
                messages.warning(request, "Title already exist")

    return render(request, 'blog/add_post.html', {'form': form, })


def get_post(request, slug):
    post = get_object_or_404(Post, slug=slug)
    comments = post.comments.order_by('-created_on').all()
    form = CommentForm()
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            Comment(author=request.user,
                    post=post,
                    content=form.cleaned_data["commentary_text"]).save()
            form = CommentForm()
    return render(request, 'blog/post.html', {'post': post,
                                              'form': form,
                                              'comments': comments,
                                              })
