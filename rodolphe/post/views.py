from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from post.models import Post
from post.forms import PostForm, DeletePostForm

# Create your views here.

def page(request):
    paginator = Paginator(Post.objects.filter(active=True, parent=None).order_by('-id'), 10)
    page_id = request.GET.get('page')
    try:
        posts = paginator.page(page_id)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    context = RequestContext(request, {
        'page': posts,
        'form': PostForm()
    })
    return render_to_response('index.html', context)

home = page

def view(request, post_id):
    post = Post.objects.get(id=int(post_id), active=True, parent=None)
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=Post.default(parent=post))
        if form.is_valid():
            form.save()
            form = PostForm()
    else:
        form = PostForm()
    context = RequestContext(request, {
        'post': post,
        'form': form
    })
    return render_to_response('post.html', context)

def new(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=Post.default())
        if form.is_valid():
            post = form.save()
            return redirect(view, post.id)
    else:
        form = PostForm()
    context = RequestContext(request, {
        'form': form
    })
    return render_to_response('new.html', context)

def edit(request, post_id):
    post = Post.objects.get(id=int(post_id), active=True)
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            old = Post.objects.get(id=post.id)
            old.id = None
            old.active = False
            old.save()
            post = form.save(commit=False)
            post.old_post = old
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
    post = Post.objects.get(id=int(post_id), active=True)
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
