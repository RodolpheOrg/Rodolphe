from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.utils.translation import ugettext as _

from main.models import Post
from main.forms import PostForm
from utils.search import get_search


def search(request):
    q, search = get_search(request)
    paginator = Paginator(Post.objects.filter(q, active=True)
                          .order_by('-created_at'), 10)
    page_id = request.GET.get('page')
    try:
        posts = paginator.page(page_id)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    context = {
        'page': posts,
        'form': PostForm(),
        'title': _('search'),
        'search': search
    }
    return render(request, 'index.html', context)
