from django.shortcuts import render_to_response
from post.models import Post

# Create your views here.

def home(request):
    return page(request)

def page(request, page_id='1'):
    context = {
        'page': page_id,
        'posts': Post.objects.filter(parent=None)
    }
    return render_to_response('index.html', context)

def post(request, post_id):
    context = {
        'post': Post.objects.get(id=int(post_id), parent=None)
    }
    return render_to_response('post.html', context)
