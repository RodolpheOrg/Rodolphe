from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from main.models import Post
from main.forms import PostForm


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
    context = {
        'page': posts,
        'form': PostForm()
    }
    return render(request, 'index.html', context)
