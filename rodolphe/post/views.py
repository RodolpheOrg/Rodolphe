from django.shortcuts import render_to_response

# Create your views here.

def home(request):
    return page(request)

def page(request, page_id='1'):
    return render_to_response('index.html', {'page': page_id})

def post(request, post_id):
    return render_to_response('post.html', {'id': post_id})
