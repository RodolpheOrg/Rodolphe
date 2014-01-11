from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from post.models import Post
from post.forms import PostForm

# Create your views here.

def home(request):
    return page(request)

def page(request, page_id='1'):
    context = RequestContext(request, {
        'page': page_id,
        'posts': Post.objects.filter(parent=None).order_by('-id'),
        'form': PostForm()
    })
    return render_to_response('index.html', context)

def view(request, post_id):
    post = Post.objects.get(id=int(post_id), parent=None)
    if request.method == 'POST':
        form = PostForm(request.POST, instance=Post.default(parent=post))
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
        form = PostForm(request.POST, instance=Post.default())
        if form.is_valid():
            form.save()
            return redirect(home)
    else:
        form = PostForm()
    context = RequestContext(request, {
        'form': form
    })
    return render_to_response('new.html', context)

def edit(request, post_id):
    p = Post.objects.get(id=int(post_id))
    if request.method == 'POST':
        form = PostForm(request.POST, instance=p)
        if form.is_valid():
            form.save()
            return redirect(view, p.thread.id)
    else:
        form = PostForm(instance=p)
    context = RequestContext(request, {
        'post': p,
        'form': form
    })
    return render_to_response('edit.html', context)
