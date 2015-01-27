from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.template import RequestContext
from django.http import HttpResponse
from django.utils import timezone

from main.models import Post
from main.forms import PostForm, DeletePostForm
from main.views.thread import view
from main.views.paging import page as home

import json


def raw(request, post_id):
    post = get_object_or_404(Post, id=int(post_id), active=True)
    infos = {
        'id': str(post.id),
        'author': str(post.author),
        'created_at': str(post.created_at),
        'updated_at': str(post.updated_at),
        'parent': str(post.parent),
        'old_post': str(post.old_post),
        'picture': str(post.picture),
        'content': str(post.content)
    }
    return HttpResponse(json.dumps(infos))


def edit(request, post_id):
    post = get_object_or_404(Post, id=int(post_id), active=True)
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            old = Post.objects.get(id=post.id)
            old.id = None
            old.active = False
            old.save()
            post = form.save(commit=False)
            post.old_post = old
            post.updated_at = timezone.now()
            post.save()
            return redirect(view, post.thread.id)
    else:
        form = PostForm(instance=post)
    context = RequestContext(request, {
        'post': post,
        'form': form
    })
    return render_to_response('edit.html', context)


def delete(request, post_id):
    post = get_object_or_404(Post, id=int(post_id), active=True)
    if request.method == 'POST':
        form = DeletePostForm(request.POST, instance=post)
        if form.is_valid():
            for resp in post.responses:
                resp.active = False
                resp.save()
            post.active = False
            post.save()
            if post.parent:
                return redirect(view, post.parent.id)
            return redirect(home)
    else:
        form = DeletePostForm(instance=post)
    context = RequestContext(request, {
        'post': post,
        'form': form
    })
    return render_to_response('delete.html', context)


def history(request, post_id):
    post = get_object_or_404(Post, id=int(post_id), active=True)
    hist = [post]
    while hist[0].old_post:
        hist.insert(0, hist[0].old_post)
    context = RequestContext(request, {
        'post': post,
        'hist': hist
    })
    return render_to_response('history.html', context)
