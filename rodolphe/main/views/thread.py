from django.shortcuts import render, redirect, get_object_or_404

from main.models import Post
from main.forms import PostForm


def view(request, post_id):
    post = get_object_or_404(Post, id=int(post_id), active=True, parent=None)
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES,
                        instance=Post.default(parent=post))
        if form.is_valid():
            resp = form.save()
            form = PostForm()
            post.last_resp_at = resp.created_at
            post.save()
    else:
        form = PostForm()
    context = {
        'post': post,
        'form': form
    }
    return render(request, 'view.html', context)


def new(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=Post.default())
        if form.is_valid():
            post = form.save()
            return redirect(view, post.id)
    else:
        form = PostForm()
    return render(request, 'new.html', {'form': form})
