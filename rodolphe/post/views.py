from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.template import RequestContext
from django.http import HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.utils.translation import get_language
from django.utils import timezone
from django.utils.translation import ugettext as _

from post.models import Post
from post.forms import PostForm, DeletePostForm

import json

# Create your views here.


def page(request):
    paginator = Paginator(Post.objects.filter(active=True, parent=None)
                          .order_by('-last_resp_at'), 10)
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
    context = RequestContext(request, {
        'post': post,
        'form': form
    })
    return render_to_response('view.html', context)


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


def about(request):
    tpl_name = 'about_{}.html'.format(get_language().split('-')[0])
    return render_to_response(tpl_name, RequestContext(request))


def markdown(request):
    examples = [
        (_("emphasis"), "*abcd*"),
        (_("emphasis"), "_abcd_"),
        (_("bold"), "**abcd**"),
        (_("underline"), "__abcd__"),
        (_("strike"), "--abcd--"),
        (_("link"), "<http://google.fr>"),
        (_("link"), "[google](http://google.fr)"),
        (_("post reference"), "&#1"),
        (_("list"), "* a\n* b\n    * c\n* d"),
        (_("ordered list"), "1. a\n2. b"),
        (_("title"), "# Title1\n## Title 2\n### Title 3\n#### Title 4\n"
         "##### Title5\n###### Title 6"),
        (_("title"), "Title 1\n=======\n\nTitle 2\n-------"),
        (_("quotation"), "> quote\n>> subquote"),
        (_("code"), "`abcd`"),
        (_("blockcode"), "    abcd\n    efgh"),
        (_("linebreak"), "------------")
    ]
    context = RequestContext(request, {
        'examples': examples
    })
    return render_to_response('markdown.html', context)
