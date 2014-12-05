from django.shortcuts import render_to_response
from django.db.models import Q
from django.template import RequestContext
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.utils.translation import ugettext as _

from main.models import Post
from main.forms import PostForm


def search(request):
    pattern = request.GET.get('q', '')
    q = Q(content__icontains=pattern)
    paginator = Paginator(Post.objects.filter(q, active=True)
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
        'form': PostForm(),
        'title': _('search'),
        'query': pattern
    })
    return render_to_response('index.html', context)
